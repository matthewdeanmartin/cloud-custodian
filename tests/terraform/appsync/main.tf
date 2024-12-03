provider "aws" {
  region = "us-east-1"
}


resource "aws_wafv2_web_acl" "example1" {
  name        = "FMManagedWebACLV2-FMS-TEST-1656966584517"
  description = "Example of a Cloudfront rate based statement."
  scope       = "REGIONAL"

  default_action {
    allow {}
  }

  rule {
    name     = "rule-1"
    priority = 1

    action {
      block {}
    }

    statement {
      rate_based_statement {
        limit              = 10000
        aggregate_key_type = "IP"

        scope_down_statement {
          geo_match_statement {
            country_codes = ["US", "NL"]
          }
        }
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = false
      metric_name                = "friendly-rule-metric-name"
      sampled_requests_enabled   = false
    }
  }

  tags = {
    Tag1 = "Value1"
    Tag2 = "Value2"
  }

  visibility_config {
    cloudwatch_metrics_enabled = false
    metric_name                = "friendly-metric-name"
    sampled_requests_enabled   = false
  }
}

resource "aws_wafv2_web_acl" "example2" {
  name        = "WebACL_TESTv2"
  description = "Example of a managed rule."
  scope       = "REGIONAL"

  default_action {
    allow {}
  }

  rule {
    name     = "rule-1"
    priority = 1

    override_action {
      count {}
    }

    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesCommonRuleSet"
        vendor_name = "AWS"

        rule_action_override {
          action_to_use {
            count {}
          }

          name = "SizeRestrictions_QUERYSTRING"
        }

        rule_action_override {
          action_to_use {
            count {}
          }

          name = "NoUserAgent_HEADER"
        }

        scope_down_statement {
          geo_match_statement {
            country_codes = ["US", "NL"]
          }
        }
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = false
      metric_name                = "friendly-rule-metric-name"
      sampled_requests_enabled   = false
    }
  }

  tags = {
    Tag1 = "Value1"
    Tag2 = "Value2"
  }

  token_domains = ["mywebsite.com", "myotherwebsite.com"]

  visibility_config {
    cloudwatch_metrics_enabled = false
    metric_name                = "friendly-metric-name"
    sampled_requests_enabled   = false
  }
}




resource "aws_appsync_graphql_api" "example0" {
  name                 = "My AppSync App"
  authentication_type  = "API_KEY"
  xray_enabled         = false

  additional_authentication_provider {
    authentication_type = "AWS_IAM"
  }

  tags = {
    waf = "test"
  }

}

#
# resource "aws_appsync_api_cache" "example" {
#   api_id               = aws_appsync_graphql_api.example0.id
#   api_caching_behavior = "FULL_REQUEST_CACHING"
#   type                 = "LARGE"
#   ttl                  = 900
# }




resource "aws_wafv2_web_acl_association" "example1_waf" {
  resource_arn = aws_appsync_graphql_api.example0.arn
  web_acl_arn  = aws_wafv2_web_acl.example1.arn
}


resource "aws_wafv2_web_acl_association" "example2_waf" {
  # resource_arn = aws_appsync_graphql_api.example0.arn
  resource_arn = aws_appsync_graphql_api.example0.arn
  web_acl_arn  = aws_wafv2_web_acl.example2.arn
  # web_acl_arn  = aws_wafv2_web_acl.example2.arn
}


#
#
# resource "aws_wafv2_web_acl_association" "example3_waf" {
#   resource_arn = aws_appsync_graphql_api.example3.arn
#   web_acl_arn  = aws_wafv2_web_acl.example2.arn
# }
