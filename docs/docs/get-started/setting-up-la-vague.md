
# Installation & set up

In this section, we're going to walk you through how you can install and set up LaVague locally.

> If you just want to test out LaVague without having to install anything locally, you can run our [Quick Tour notebook with Google Colab](https://colab.research.google.com/github/lavague-ai/lavague/blob/main/docs/docs/get-started/quick-tour.ipynb).

## Step 1: Preparing your environment

LaVague currently supports only Selenium as a web automation tool, which requires users to first install a webdriver to interface with the chosen browser (Chrome, Firefox, etc.).

In this guide, we will walk you through two installation options: 
- Either you can either run LaVague within [our pre-configured dev container](#run-lavague-with-our-dev-container) which will handle the webdriver installation for you
- Or you can do this webdriver [installation manually](#installing-the-webdriver-locally)

### Running LaVague with our Dev container

⚠️ Pre-requisites:
- 🐋 Docker: Ensure Docker is installed and running on your machine. Docker is used to create and manage your development container
- Visual Studio Code
- Visual Studio Code's Remote - Containers Extension: You can download this extension by searching for it within the Extensions view

To open the project in our dev container you need to:

1. Open VSCode at the root of the LaVague repo.
2. Click on the blue "><" icon in the bottom left corner, then select "Reopen in Container" in the drop-down menu that then appears.

VS Code will then build the container based on the Dockerfile and devcontainer.json files in the .devcontainer folder. This process might take a few minutes the first time you run it.

### Installing the webdriver locally

An alternative option is to manually install the webdriver. The following instructions are valid for users working on Debian-based Linux distributions. For instructions on how to install a driver on a different OS or distribution, [see the Selenium documentation](https://selenium-python.readthedocs.io/installation.html#drivers)

You may first need to update the list of available packages for your system:

```
sudo apt update
```

Next, you will need to make sure you have the following packages installed on your system:
```
sudo apt install -y ca-certificates fonts-liberation unzip \
libappindicator3-1 libasound2 libatk-bridge2.0-0 libatk1.0-0 libc6 \
libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgbm1 \
libgcc1 libglib2.0-0 libgtk-3-0 libnspr4 libnss3 libpango-1.0-0 \
libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 \
libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 \
libxrandr2 libxrender1 libxss1 libxtst6 lsb-release wget xdg-utils`
```

Now you can download the necessary files for the Chrome webdriver with the following code:
```
wget https://storage.googleapis.com/chrome-for-testing-public/122.0.6261.94/linux64/chrome-linux64.zip
wget https://storage.googleapis.com/chrome-for-testing-public/122.0.6261.94/linux64/chromedriver-linux64.zip
unzip chrome-linux64.zip
unzip chromedriver-linux64.zip
rm chrome-linux64.zip chromedriver-linux64.zip
```

Finally, we will move the unzipped folders to our root directory, as this is where LaVague expects them to be found by default:
```
mv chrome-linux64/ ~/
mv chromedriver-linux64/ ~/
```

> For instructions on how to install a driver on a different OS, [see the Selenium documentation](https://selenium-python.readthedocs.io/installation.html#drivers)

## Step 2: Installing LaVague

To install LaVague from the latest version of the code on `main`, run the following:

```
git clone https://github.com/lavague-ai/LaVague.git
pip install -e LaVague
```

> Note that we install LaVague from the latest GitHub commit on main for now to be sure we have the very latest files at this early fast-moving stage of the project. However, we do provide a PyPi package and will move to installing the package via pip once the project is more stable.

## Conclusions

You are now ready to use LaVague with the integration of your choice. To see how to do this with our CLI, see our [quick tour](./quick-tour.ipynb) or [integration pages](../integrations/hugging-face-api.ipynb).

> Note that these example scripts may come with additional requirements, such as inputting an API key into the script before they will run successfully. Please check the comments in the script you want to test before running in.