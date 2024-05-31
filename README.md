# GPT agent

## export OPEN API Key
```bash
echo "export OPENAI_API_KEY='API키'" >> ~/.bashrc
source ~/.bashrc
```


## create virtual env 

```bash
pip3 install virtualenv
```

```bash
cd voice_agent
virtualenv venv -p python3.8
source venv/bin/activate
```


## Prerequisites

```bash
sudo apt install portaudio19-dev
pip install -r requirements.txt
```

## Usage <a name = "usage"></a>

```bash
source venv/bin/activate
cd sw-voice-agent
chmod +x command.sh
./command.sh
```

