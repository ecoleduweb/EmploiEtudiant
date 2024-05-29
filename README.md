# Système de déploiment et de build Github Actions
Dans ce readme, vous allez retrouver certaines erreurs possibles et leurs résolutions.
### Si vous rencontrez l'erreur suivante lors de l'installation des requirements.txt
```bash
err: error: externally-managed-environment
err: 
err: × This environment is externally managed
err: ╰─> To install Python packages system-wide, try apt install
err:     python3-xyz, where xyz is the package you are trying to
err:     install.
err:     
err:     If you wish to install a non-Debian-packaged Python package,
err:     create a virtual environment using python3 -m venv path/to/venv.
err:     Then use path/to/venv/bin/python and path/to/venv/bin/pip. Make
err:     sure you have python3-full installed.
err:     
err:     If you wish to install a non-Debian packaged Python application,
err:     it may be easiest to use pipx install xyz, which will manage a
err:     virtual environment for you. Make sure you have pipx installed.
err:     
err:     See /usr/share/doc/python3.11/README.venv for more information.
err: 
err: note: If you believe this is a mistake, please contact your Python installation or OS distribution provider. You can override this, at the risk of breaking your Python installation or OS, by passing --break-system-packages.
```
La commande suivante devrait régler votre problème:
```bash
sudo rm /usr/lib/python3.*/EXTERNALLY-MANAGED
```

### Si vous rencontrez un problème avec SSH et que vous avez cette erreur:
```
ssh: handshake failed: ssh: unable to authenticate, attempted methods [none publickey], no supported methods remain
```

Vous devez vous assurer que la clé SSH publique du serveur est dans les **authorized_keys** du même serveur. Si ce n'est pas le cas, vous pouvez effectuer la modification avec cette commande:
```bash
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
```
Noubliez pas de redémarrer le service SSH par la suite!
```bash
sudo systemctl restart ssh.service
```
