{ pkgs, lib, config, inputs, ... }: {
  packages = [ ];

  enterShell = ''
    if [ ! -f back/.env ]; then
      cp back/.env.example back/.env
      sed -i 's/supermotdepasse/tekiens_net/g' back/.env
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
    directory = "./back";
    venv = {
      enable = true;
      requirements = ./back/requirements.txt;
    };
  };

  languages.javascript = {
    enable = true;
    directory = "./front";
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
