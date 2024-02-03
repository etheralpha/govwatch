# This plugin will wrap input in badge with custum color derived from input
# 
# Usage:
#   category = "Genral"
#   {{ category | badge }}
# 
# Output:
#   <span class='badge' style='border-color: #a53fb1!important'>General</span>

require 'digest/md5'

module Jekyll
  module Badge

    def badge(input, classes=nil)
      color = Digest::MD5.hexdigest(input)[0..5]
      "<span class='badge #{classes}' style='border-color: ##{color}!important'>#{input}</span>"
    end

  end
end

Liquid::Template.register_filter(Jekyll::Badge)