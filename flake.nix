{
  description = "Application packaged using poetry2nix";

  inputs.flake-utils.url = "github:numtide/flake-utils";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  inputs.poetry2nix = {
    url = "github:nix-community/poetry2nix";
    inputs.nixpkgs.follows = "nixpkgs";
  };
  inputs.mach-nix = {
    url = "github:DavHau/mach-nix/3.5.0";
    inputs.pypi-deps-db.url = "github:DavHau/pypi-deps-db/e9571cac25d2f509e44fec9dc94a3703a40126ff";
    inputs.nixpkgs.follows = "nixpkgs";
    inputs.flake-utils.follows = "flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix, mach-nix }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          overlays = [ poetry2nix.overlay ];
        };
      in rec {
        packages = {
          # rawpython = pkgs.python310.withPackages (ps: with ps; [numpy poetry]);

          # mxpython = mach-nix.lib.${system}.mkPython {
          #   requirements = ''              
          #     poetry => 1.3.0
          #   '';
          #   python = "python310";
          #   ignoreCollisions = true;
          #   ignoreDataOutdated = true;
          # };

          ppopython = pkgs.poetry2nix.mkPoetryEnv {
            python = pkgs.pypy3;
            projectDir = ./.;
            editablePackageSources = {
              aoc = ./.;
            };
            preferWheels = true;
            # extraPackages = (ps: [ ps.wheel ]);
            # extraPackages = (ps: [ ps.poetry ]);
            # ignoreCollisions = true;
          };

          popython = pkgs.poetry2nix.mkPoetryEnv {
            python = pkgs.python310;
            projectDir = ./.;
            editablePackageSources = {
              aoc = ./.;
            };
            preferWheels = true;
            # extraPackages = (ps: [ ps.poetry ]);
            # ignoreCollisions = true;
          };
        };
        defaultPackage = packages.popython;

        devShell = pkgs.mkShell {
          buildInputs = with pkgs; [
            # zlib
            # poetry
            # (python310.withPackages (ps: [ps.numpy]))
            defaultPackage
            # (poetry.override {python = defaultPackage;})
          ];
        };
      });
}
