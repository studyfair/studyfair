# frozen_string_literal: true

ActiveAdmin.register Assignment do
  actions :all

  controller do
    def scoped_collection
      resource_class.for(current_user)
    end
  end

  member_action :report, method: :get do
    s3_client = Aws::S3::Client.new

    object = s3_client.get_object(bucket: Rails.env.to_sym, key: resource.report_storage_key)

    render locals: { assignment: resource.decorate(context: { raw_report: object.body.read }) }
  end

  permit_params :title, :course_id, options: %i[ngram_size threshold]

  index do
    selectable_column

    column :course
    column :title

    column :report do |assignment|
      if assignment.has_report?
        link_to "view", report_admin_assignment_url(assignment), target: "_blank", rel: "noopener"
      else
        "N/A"
      end
    end

    actions
  end

  form do |f|
    f.semantic_errors

    f.inputs do
      input :title
      input :course_id, as: :select,
        collection: Course.all.for(current_user).map { |c| [c.title, c.id] },
        include_blank: false
    end

    f.actions
  end
end
