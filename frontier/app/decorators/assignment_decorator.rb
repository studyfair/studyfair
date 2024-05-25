# frozen_string_literal: true

class AssignmentDecorator < ApplicationDecorator
  delegate_all

  def submission_field(code_fragment)
    submission = code_fragment.submission
    upload = code_fragment.upload

    if submission
      h.link_to "#{submission.id} (#{upload.filename})", h.admin_submission_url(submission)
    else
      "-"
    end
  end

  delegate :report, to: :report_builder

  def algorithm
    report_builder.algorithm || object.nicad
  end

  private

    def report_builder
      @report_builder ||= ReportBuilder.build(context[:raw_report])
    end
end
