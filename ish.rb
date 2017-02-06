class Ish < Formula
  url "https://github.com/grahamc/ish.git", :ref => 'master'
  version '0.1.3'

  depends_on :python3

  resource "boto3" do
    url "https://pypi.python.org/packages/source/b/boto3/boto3-1.1.3.tar.gz"
    sha256 "10b5d92ce79366425e35af0b79b001b8ebc38c5fca6c7742885f6b8f87d06665"
  end

  resource "botocore" do
    url "https://pypi.python.org/packages/source/b/botocore/botocore-1.2.4.tar.gz"
    sha256 "6330dec53831e4f961e2503a4d9bfe9e790e1e7ac716f8edc07f1b37ff2765da"
  end

  resource "docutils" do
    url "https://pypi.python.org/packages/source/d/docutils/docutils-0.12.tar.gz"
    sha256 "c7db717810ab6965f66c8cf0398a98c9d8df982da39b4cd7f162911eb89596fa"
  end

  resource "futures" do
    url "https://pypi.python.org/packages/source/f/futures/futures-2.2.0.tar.gz"
    sha256 "151c057173474a3a40f897165951c0e33ad04f37de65b6de547ddef107fd0ed3"
  end

  resource "jmespath" do
    url "https://pypi.python.org/packages/source/j/jmespath/jmespath-0.7.1.tar.gz"
    sha256 "cd5a12ee3dfa470283a020a35e69e83b0700d44fe413014fd35ad5584c5f5fd1"
  end

  resource "python-dateutil" do
    url "https://pypi.python.org/packages/source/p/python-dateutil/python-dateutil-2.4.2.tar.gz"
    sha256 "3e95445c1db500a344079a47b171c45ef18f57d188dffdb0e4165c71bea8eb3d"
  end

  resource "six" do
    url "https://pypi.python.org/packages/source/s/six/six-1.9.0.tar.gz"
    sha256 "e24052411fc4fbd1f672635537c3fc2330d9481b18c0317695b46259512c91d5"
  end

  def install
    version = Language::Python.major_minor_version "python3"
    ENV.prepend_create_path "PYTHONPATH", libexec/"vendor/lib/python#{version}/site-packages"


    %w[boto3 botocore docutils futures jmespath python-dateutil six].each do |r|
      resource(r).stage do
        system "python3", *Language::Python.setup_install_args(libexec/"vendor")
      end
    end
    ENV.prepend_create_path "PYTHONPATH", libexec/"lib/python#{version}/site-packages"
    system "python3", *Language::Python.setup_install_args(libexec)

    bin.install Dir[libexec/"bin/*"]
    bin.env_script_all_files(libexec/"bin", :PYTHONPATH => ENV["PYTHONPATH"])
    etc.install Dir["contrib/ish-autocomplete"]
  end

  def caveats
    "Source #{etc}/ish-autocomplete for autocompletion"
  end
end
