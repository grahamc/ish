class Ish < Formula
  url "https://github.com/grahamc/ish.git", :ref => 'master'
  version '0.1.2'

  depends_on :python3

  resource "boto3" do
    url "https://pypi.python.org/packages/source/b/boto3/boto3-1.1.3.tar.gz"
    sha1 "be8bb2154af0589d4a19231412cfec07c60252b3"
  end

  resource "botocore" do
    url "https://pypi.python.org/packages/source/b/botocore/botocore-1.2.4.tar.gz"
    sha1 "22d04c5adaa01ac3e5229b5ece14785799b1add9"
  end

  resource "docutils" do
    url "https://pypi.python.org/packages/source/d/docutils/docutils-0.12.tar.gz"
    sha1 "002450621b33c5690060345b0aac25bc2426d675"
  end

  resource "futures" do
    url "https://pypi.python.org/packages/source/f/futures/futures-2.2.0.tar.gz"
    sha1 "0302253fb7e4fbbc48000b3e3dde244e9e7cd353"
  end

  resource "jmespath" do
    url "https://pypi.python.org/packages/source/j/jmespath/jmespath-0.7.1.tar.gz"
    sha1 "10cbbf7f1a892d2c4fce7f7e84bb91e9108fcf45"
  end

  resource "python-dateutil" do
    url "https://pypi.python.org/packages/source/p/python-dateutil/python-dateutil-2.4.2.tar.gz"
    sha1 "1d975f5db65306a61f4353ef00308ec806f47f54"
  end

  resource "six" do
    url "https://pypi.python.org/packages/source/s/six/six-1.9.0.tar.gz"
    sha1 "d168e6d01f0900875c6ecebc97da72d0fda31129"
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
