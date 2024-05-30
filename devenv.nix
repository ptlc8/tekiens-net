{ pkgs, lib, config, inputs, ... }: {
  packages = [ ];

  enterShell = ''
    if [ ! -f src/.env ]; then
      cp src/.env.example src/.env
      sed -i 's/supermotdepasse/tekiens_net/g' src/.env
    fi
  '';

  services.mysql = {
    enable = true;
    initialDatabases = [{
      name = "tekiens_net";
      schema = ./init.sql;
    }];
    ensureUsers = [{
      name = "tekiens_net";
      password = "tekiens_net";
      ensurePermissions."tekiens_net.*" = "ALL PRIVILEGES";
    }];
  };

  languages.python = {
    enable = true;
    directory = "./src";
    venv = {
      enable = true;
      requirements = ./src/requirements.txt;
    };
  };

  languages.javascript = {
    enable = true;
    directory = "./src/front";
    npm = {
      enable = true;
      install.enable = true;
    };
  };

  processes = {
    backend.exec =
      "cd ${config.languages.python.directory} && python3 -m flask run";
    frontend.exec =
      "cd ${config.languages.javascript.directory} && npx vite build --watch";
  };
}
