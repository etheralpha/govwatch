# This plugin will remove uncommon characters
# 
# Usage:
#   title = "how to: a guide to upskilling - 3rd edition 📚"
#   <h1>{{ title | stripspecialchars }}</h1>
# 
# Output:
#   how to: a guide to upskilling - 3rd edition

module Jekyll
  module StripSpecialCharacters

    def stripspecialchars(input)
      input.gsub(/[^0-9a-z,-: ]/i, '').strip
    end

  end
end

Liquid::Template.register_filter(Jekyll::StripSpecialCharacters)