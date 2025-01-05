{ 
  description = "A Nix-flake-based Python development environment with codecrafters";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-24.11";
  };

  outputs = { nixpkgs, ... }: let
    # system should match the system you are running on
    # system = "x86_64-linux";
    system = "aarch64-darwin";
  in {
    devShells."${system}".default = let
      pkgs = import nixpkgs {
        inherit system;
      };
    in pkgs.mkShell {
      # Create an environment with Python 3.13 and codecrafters-cli
      packages = with pkgs; [
        python313
        codecrafters-cli
      ] ++ (with pkgs.python313Packages; [
        pip
        pipenv
        venvShellHook
      ]);

      shellHook = ''
        echo "AMe2 -+"
        echo "Python version: `${pkgs.python313}/bin/python --version`"
        echo "Using codecrafters-cli"
        exec zsh 
      '';
    };
  };
}
