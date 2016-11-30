require_relative '../../helper_spec.rb'
require 'yaml'

## Load files from remote machine
extra_advanced_team_db = cat_remote_file("/tmp/extra_advanced_team_db.yaml")

describe "Database match for extra teams" do
  it "extra variables" do
    expected_hash = [{ "bla"=> "xxxx", "name"=> "daniels", "state"=> "present" },{ "extra_xxxx"=> "xxx", "name"=> "gin", "state"=> "present" }, { "name"=> "ops", "openvpn"=> true, "state"=> "present"}, {"name"=> "label", "openvpn"=> true, "state"=> "present"}]
    given_hash = YAML.load(extra_advanced_team_db)
    expect(given_hash).to match(expected_hash)
  end

end