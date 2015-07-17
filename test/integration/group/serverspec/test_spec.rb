require 'serverspec'

# Required by serverspec
set :backend, :exec


describe group('group1') do
  it { should exist }
  it { should have_gid 5000 }
end

describe group('group2') do
  it { should exist }
  it { should have_gid 5001 }
end

describe group('group3') do
  it { should exist }
  it { should have_gid 5002 }
end

describe group('group4') do
  it { should_not exist }
end