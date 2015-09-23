class Ish < Formula
  url "https://github.com/grahamc/ish.git", :ref => 'master'
  version '0.1.0'

  depends_on :python3

  resource "boto3" do
    url "https://pypi.python.org/packages/source/b/boto3/boto3-1.1.3.tar.gz"
    sha1 "be8bb2154af0589d4a19231412cfec07c60252b3"
  end

  def install
    version = Language::Python.major_minor_version "python3"
    ENV.prepend_create_path "PYTHONPATH", libexec/"vendor/lib/python#{version}/site-packages"


    %w[boto3].each do |r|
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
