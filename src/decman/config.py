"""
Module for decman configuration options.

NOTE: Do NOT use from imports as global variables might not work as you expect.

Only use:

import decman.config

or

import decman.config as whatever

-- Configuring commands --

Commands are stored as methods in the Commands-class.
The global variable 'commands' of this module is an instance of the Commands-class.

To change the defalts, create a new child class of the Commands-class and set the 'commands'
variable to an instance of your class. Look in the README for examples.
"""

import typing


class Commands:
    """
    Default commands.
    """

    def list_pkgs(self) -> list[str]:
        """
        Running this command outputs a newline seperated list of explicitly installed packages.
        """
        return ["pacman", "-Qeq", "--color=never"]

    def list_foreign_pkgs_versioned(self) -> list[str]:
        """
        Running this command outputs a newline seperated list of installed packages and their
        versions that are not from pacman repositories.
        """
        return ["pacman", "-Qm", "--color=never"]

    def install_pkgs(self, pkgs: list[str]) -> list[str]:
        """
        Running this command installs the given packages from pacman repositories.
        """
        return ["pacman", "-S", "--asexplicit"] + pkgs

    def install_files(self, pkg_files: list[str]) -> list[str]:
        """
        Running this command installs the given packages files.
        """
        return ["pacman", "-U", "--asdeps"] + pkg_files

    def set_as_explicitly_installed(self, pkgs: list[str]) -> list[str]:
        """
        Running this command installs sets the given as explicitly installed.
        """
        return ["pacman", "-D", "--asexplicit"] + pkgs

    def install_deps(self, deps: list[str]) -> list[str]:
        """
        Running this command installs the given packages from pacman repositories.
        The packages are installed as dependencies.
        """
        return ["pacman", "-S", "--needed", "--asdeps"] + deps

    def is_installable(self, pkg: str) -> list[str]:
        """
        This command exits with code 0 when a package is installable from pacman repositories.
        """
        return ["pacman", "-Sddp", pkg]

    def upgrade(self) -> list[str]:
        """
        Running this command upgrades all pacman packages.
        """
        return ["pacman", "-Syu"]

    def remove(self, pkgs: list[str]) -> list[str]:
        """
        Running this command removes the given packages and their dependencies
        (that aren't required by other packages).
        """
        return ["pacman", "-Rs"] + pkgs

    def enable_units(self, units: list[str]) -> list[str]:
        """
        Running this command enables the given systemd units.
        """
        return ["systemctl", "enable", "--now", "--quiet"] + units

    def disable_units(self, units: list[str]) -> list[str]:
        """
        Running this command disables the given systemd units.
        """
        return ["systemctl", "disable", "--quiet"] + units

    def enable_user_units(self, units: list[str]) -> list[str]:
        """
        Running this command enables the given systemd units for the user it's run as.
        """
        return ["systemctl", "enable", "--now", "--quiet", "--user"] + units

    def disable_user_units(self, units: list[str]) -> list[str]:
        """
        Running this command disables the given systemd units fol the user it's run as.
        """
        return ["systemctl", "disable", "--quiet"] + units

    def compare_versions(self, installed_version: str,
                         new_version: str) -> list[str]:
        """
        Running this command outputs -1 when the installed version is older than the new version.
        """
        return ["vercmp", installed_version, new_version]

    def git_clone(self, repo: str, dest: str) -> list[str]:
        """
        Running this command clones a git repository to the the given destination.
        """
        return ["git", "clone", repo, dest]

    def git_diff(self, from_commit: str) -> list[str]:
        """
        Running this command outputs the difference between the given commit and
        the current state of the repository.
        """
        return ["git", "diff", from_commit]

    def git_get_commit_id(self) -> list[str]:
        """
        Running this command outputs the current commit id.
        """
        return ["git", "rev-parse", "HEAD"]

    def review_file(self, file: str) -> list[str]:
        """
        Running this command outputs a file for the user to see.
        """
        return ["less", file]

    def make_chroot(self, chroot_root_dir: str,
                    with_pkgs: list[str]) -> list[str]:
        """
        Running this command creates a new arch chroot to the chroot directory and installs the
        given packages there.
        """
        return ["mkarchroot", chroot_root_dir] + with_pkgs

    def make_chroot_pkg(self, chroot_dir: str, user: str,
                        pkgfiles_to_install: list[str]) -> list[str]:
        """
        Running this command creates a package file using the given chroot.
        The package is created as the user and the pkg_files_to_install are installed
        in the chroot before the package is created.
        """
        makechrootpkg_cmd = ["makechrootpkg", "-r", chroot_dir, "-U", user]

        for pkgfile in pkgfiles_to_install:
            makechrootpkg_cmd += ["-I", pkgfile]

        return makechrootpkg_cmd


commands: Commands = Commands()
debug_output: bool = False
quiet_output: bool = False

valid_pkgexts: list[str] = [
    ".pkg.tar",
    ".pkg.tar.gz",
    ".pkg.tar.bz2",
    ".pkg.tar.xz",
    ".pkg.tar.zst",
    ".pkg.tar.lzo",
    ".pkg.tar.lrz",
    ".pkg.tar.lz4",
    ".pkg.tar.lz",
    ".pkg.tar.Z",
]

makepkg_user: str = "nobody"
build_dir: str = "/tmp/decman/build"
pkg_cache_dir: str = "/var/cache/decman"
aur_rpc_timeout: typing.Optional[int] = 30
