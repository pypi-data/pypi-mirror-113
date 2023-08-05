from pgtoolkit import conf, pgpass

from . import db, exceptions, hookimpl
from .ctx import BaseContext
from .models import interface
from .models.system import Instance, InstanceSpec, PostgreSQLInstance
from .types import ConfigChanges, Role


@hookimpl  # type: ignore[misc]
def instance_configure(
    ctx: BaseContext,
    instance: InstanceSpec,
    config: conf.Configuration,
    changes: ConfigChanges,
) -> None:
    """Set / update passfile entry for PostgreSQL roles upon instance
    configuration.

    This handles the entry for super-user role, if configured accordingly.

    If a role should be referenced in password file, we either create an entry
    or update the existing one to reflect configuration changes (e.g. port
    change).
    """

    try:
        old_port, port = changes["port"]
    except KeyError:
        old_port = port = config.get("port", 5432)
    assert isinstance(port, int)

    surole = ctx.settings.postgresql.surole
    with pgpass.edit(ctx.settings.postgresql.auth.passfile) as passfile:
        surole_entry = None
        if old_port is not None:
            # Port changed, update all entries matching the old value.
            assert isinstance(old_port, int)
            for entry in passfile:
                if entry.matches(port=old_port):
                    if entry.matches(username=surole.name):
                        surole_entry = entry
                    entry.port = port
        if surole.pgpass and surole_entry is None and surole.password:
            # No previous entry for super-user, add one.
            password = surole.password.get_secret_value()
            entry = pgpass.PassEntry("*", port, "*", surole.name, password)
            passfile.lines.append(entry)
            passfile.sort()


@hookimpl  # type: ignore[misc]
def instance_drop(ctx: BaseContext, instance: Instance) -> None:
    """Remove password file (pgpass) entries for the instance being dropped."""
    passfile_path = ctx.settings.postgresql.auth.passfile
    with pgpass.edit(passfile_path) as passfile:
        passfile.remove(port=instance.port)
    if not passfile.lines:
        passfile_path.unlink()


def apply(ctx: BaseContext, instance: Instance, role_manifest: interface.Role) -> None:
    """Apply state described by specified role manifest as a PostgreSQL instance.

    The instance should be running.
    """
    if role_manifest.state == interface.Role.State.absent:
        if exists(ctx, instance, role_manifest.name):
            drop(ctx, instance, role_manifest.name)
        return None

    if not exists(ctx, instance, role_manifest.name):
        create(ctx, instance, role_manifest)
    if role_manifest.password:
        if not has_password(ctx, instance, role_manifest):
            set_password_for(ctx, instance, role_manifest)
    set_pgpass_entry_for(ctx, instance, role_manifest)


def describe(ctx: BaseContext, instance: Instance, name: str) -> interface.Role:
    """Return a role described as a manifest.

    :raises ~exceptions.RoleNotFound: if no role with specified 'name' exists.
    """
    if not exists(ctx, instance, name):
        raise exceptions.RoleNotFound(name)
    role = interface.Role(name=name)
    if has_password(ctx, instance, role):
        role = role.copy(update={"password": "<set>"})
    if in_pgpass(ctx, instance, role):
        role = role.copy(update={"pgpass": True})
    return role


def drop(ctx: BaseContext, instance: Instance, name: str) -> None:
    """Drop a role from instance.

    :raises ~exceptions.RoleNotFound: if no role with specified 'name' exists.
    """
    if not exists(ctx, instance, name):
        raise exceptions.RoleNotFound(name)
    with db.connect(instance, ctx.settings.postgresql.surole) as cnx:
        with cnx.cursor() as cur:
            cur.execute(db.query("role_drop", username=name))
        cnx.commit()
    role = interface.Role(name=name, pgpass=False)
    set_pgpass_entry_for(ctx, instance, role)


def exists(ctx: BaseContext, instance: Instance, name: str) -> bool:
    """Return True if named role exists in 'instance'.

    The instance should be running.
    """
    with db.connect(instance, ctx.settings.postgresql.surole) as cnx:
        with cnx.cursor() as cur:
            cur.execute(db.query("role_exists"), {"username": name})
            return cur.rowcount == 1  # type: ignore[no-any-return]


def has_password(ctx: BaseContext, instance: Instance, role: Role) -> bool:
    """Return True if the role has a password set."""
    with db.connect(instance, ctx.settings.postgresql.surole) as cnx:
        with cnx.cursor() as cur:
            cur.execute(db.query("role_has_password"), {"username": role.name})
            (haspassword,) = cur.fetchone()
            return haspassword  # type: ignore[no-any-return]


def create(ctx: BaseContext, instance: Instance, role: Role) -> None:
    """Create 'role' in 'instance'.

    The instance should be running and the role should not exist already.
    """
    if role.password is not None:
        query = "role_create"
        args = {"password": role.password.get_secret_value()}
    else:
        query = "role_create_no_password"
        args = {}
    with db.connect(instance, ctx.settings.postgresql.surole) as cnx:
        with cnx.cursor() as cur:
            cur.execute(db.query(query, username=role.name), args)
        cnx.commit()


def set_password_for(
    ctx: BaseContext, instance: PostgreSQLInstance, role: Role
) -> None:
    """Set password for a PostgreSQL role on instance."""
    if role.password is None:
        return

    with db.connect(instance, ctx.settings.postgresql.surole) as conn:
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(
                db.query("role_alter_password", username=role.name),
                {"password": role.password.get_secret_value()},
            )


def in_pgpass(ctx: BaseContext, instance: Instance, role: Role) -> bool:
    """Return True if 'role' is present in password file for 'instance'."""
    port = int(instance.config().port)  # type: ignore[arg-type]
    passfile = pgpass.parse(ctx.settings.postgresql.auth.passfile)
    return any(entry.matches(username=role.name, port=port) for entry in passfile)


def set_pgpass_entry_for(ctx: BaseContext, instance: Instance, role: Role) -> None:
    """Add, update or remove a password file entry for 'role' of 'instance'."""
    port = int(instance.config().port)  # type: ignore[arg-type]

    username = role.name
    password = None
    if role.password:
        password = role.password.get_secret_value()
    with pgpass.edit(ctx.settings.postgresql.auth.passfile) as passfile:
        for entry in passfile:
            if entry.matches(username=username, port=port):
                if not role.pgpass:
                    passfile.lines.remove(entry)
                elif password is not None:
                    entry.password = password
                break
        else:
            if role.pgpass and password is not None:
                entry = pgpass.PassEntry("*", port, "*", username, password)
                passfile.lines.append(entry)
        passfile.sort()
