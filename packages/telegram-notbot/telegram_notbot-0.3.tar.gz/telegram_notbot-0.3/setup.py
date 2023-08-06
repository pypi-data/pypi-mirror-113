from distutils.core import setup
setup(
    name = 'telegram_notbot',
    packages = ['telegram_notbot'],
    version = '0.3',
    license='MIT',
    description = 'Send messages to telegram users that contact the bot',
    author = 'José Patrício',
    author_email = 'jpegx100@gmail.com',
    url = 'https://github.com/zehpatricio/telegram_notbot',
    download_url = 'https://github.com/zehpatricio/telegram_notbot/archive/refs/tags/0.3.tar.gz',
    keywords = ['Telegram', 'bot', 'notify'],
    install_requires=[
        'requests'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8',
    ],
)