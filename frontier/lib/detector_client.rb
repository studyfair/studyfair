# frozen_string_literal: true

class DetectorClient
  REQUEST_IDENTIFIER_HEADER = "Request-ID"
  private_constant :REQUEST_IDENTIFIER_HEADER

  include HTTParty

  headers "Content-Type" => "application/json"

  def initialize(config)
    @config = config
    @access_token = config.fetch(:access_token)

    self.class.base_uri config.fetch(:base_uri)
  end

  def detect(submission)
    request_body = request_body(submission).to_json

    with_request_identifier do |request_identifier|
      self.class.post(
        "/detection/compare-repositories",
        body: request_body,
        headers: {
          "Authorization" => authorization_value(access_token),
          REQUEST_IDENTIFIER_HEADER => request_identifier
        }
      )
    end
  end

  private

    def request_body(submission)
      {
        "algorithm" => {
          "name" => "LCS",
          "params" => {
            "n" => 2,
            "threshold" => 0.45
          }
        },
        "assignment" => submission.storage_key,
        "repository" => submission.assignment.storage_key
      }
    end

    def authorization_value(access_token)
      "Bearer #{access_token}"
    end

    def with_request_identifier
      yield SecureRandom.uuid
    end

    attr_reader :config, :access_token
end
