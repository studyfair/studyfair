# frozen_string_literal: true

class AssignmentDecoratorLegacy < ApplicationDecorator
  include Memery

  ITEM_ATTRIBUTES = %i[
    revision
    file_name
    class_name
    function_name
    function_start
    function_end
  ].freeze

  Report = Struct.new(:clusters, keyword_init: true)
  Cluster = Struct.new(:items, keyword_init: true)
  Item = Struct.new(*ITEM_ATTRIBUTES, keyword_init: true) do
    def initialize(...)
      super

      %i[class_name function_name].each do |attribute|
        public_send(:"#{attribute}=", handle_blank(public_send(attribute)))
      end
    end

    private

      def handle_blank(value)
        value.presence || "—"
      end
  end

  delegate_all

  memoize def report
    parsed_report = JSON.parse(context[:raw_report], symbolize_names: true)

    # metadata = parsed_report[:metadata]
    clusters = parsed_report[:clusters]

    clusters = clusters.map do |raw_cluster|
      items = raw_cluster.map do |raw_item|
        Item.new(raw_item.transform_keys(&:to_s).transform_keys(&:underscore))
      end

      Cluster.new(items:)
    end

    Report.new(clusters:)
  end
end
