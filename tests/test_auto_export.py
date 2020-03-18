import pytest
import boto3
import sys
from moto import mock_s3
from moto import mock_ses
from moto import mock_dynamodb2
import botocore.errorfactory

sys.path.append('./dot-sdc-auto-export')
from dot_sdc_auto_export import lambda_function
import os

Origin_Bucket_Name = os.environ.get('WYDOT_TEAM_BUCKET')
Export_Bucket_Name = os.environ.get('WYDOT_AUTOEXPORT_BUCKET')

try:
    os.mkdir('/tmp')
except:
    pass

@mock_s3
def setup_raw_submissions():
    boto3.setup_default_session()
    conn = boto3.client('s3', region_name='us-east-1')
    conn.create_bucket(Bucket=Origin_Bucket_Name)
    conn.create_bucket(Bucket=Export_Bucket_Name)
    return conn

@mock_dynamodb2
def setup_dynamodb_table():
    dynamodb_client = boto3.client('dynamodb', region_name='us-east-1')
    dynamodb_client.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'Name',
                'AttributeType': 'S'
            }
        ],
        TableName=os.environ.get('DYNAMODB_AVAILABLE_DATASET'),
        KeySchema=[
            {
                'AttributeName': 'Name',
                'KeyType': 'HASH'
            }
        ]

    )

    dynamodb_client.put_item(
        TableName=os.environ.get('DYNAMODB_AVAILABLE_DATASET'),
        Item={
            'Name': {'S': 'FirstTest'},
            'exportWorkflow': {
                'M': {'BadTest': {'S': 'BadData'}}
            }
        }
    )

    dynamodb_client.put_item(
        TableName=os.environ.get('DYNAMODB_AVAILABLE_DATASET'),
        Item={
            'Name': {'S': 'Test'},
            'exportWorkflow': {
                'M': {"CVP" : { "M" : {      "THEA" : { "M" : {          "datatypes" : { "M" : {              "BSM" : { "M" : {                  "NonTrusted" : { "M" : {                      "WorkflowStatus" : { "S" : "NotifyReview" }                    }                  },                  "Trusted" : { "M" : {                      "WorkflowStatus" : { "S" : "NotifyReview" }                    }                  }                }              },              "SPAT" : { "M" : {                  "NonTrusted" : { "M" : {                      "WorkflowStatus" : { "S" : "Notify" }                    }                  },                  "Trusted" : { "M" : {                      "WorkflowStatus" : { "S" : "NotifyReview" }                    }                  }                }              }            }          },          "ListOfPOC" : { "L" : [              { "S" : "srinivas.nannapaneni@reancloud.com" },              { "S" : "akbar.sheik@reancloud.com" },              { "S" : "santosh.karla@reancloud.com" },              { "S" : "swarnadee.bapat@reancloud.com" }            ]          },          "UpdateDate" : { "S" : "08-06-2018" },          "UsagePolicyDesc" : { "S" : "<p>The THEA DOT is providing ongoing access to data generated by the Connected Vehicle Pilot deployment to support performance measurement and evaluation activities to a select group of explicitly approved individuals.  The CV Pilot is an ongoing research activity and includes access to rapidly evolving data sets and products. THEA DOT makes no claims, promises or guarantees about the accuracy, completeness, or adequacy of the contents of data and expressly disclaims liability for errors and omissions in the data.</p><p>Conducting research activities on THEA DOT CV pilot data and resources is restricted to authorized individuals for the purpose for which access was granted.  Further, users of the THEA CV Pilot data are expected to use good judgment and research practices. This includes but is not limited to:<li>Using CV Pilot data in a lawful and appropriate manner<li>Respecting the rights and privacy of others<li>Maintaining the CV Pilot data in an appropriate manner including accessing the Secure Data Commons through proper authentication<li>Including appropriate citations to THEA DOT&#39;s Connected Vehicle Pilot when using data or results derived from the data<li>No data or derived results from the THEA data shall be exported or removed from the SDC in anyway without the express approval of the THEA DOT CV Pilot</p>" }        }      },      "WYDOT" : { "M" : {          "datatypes" : { "M" : {              "ALERT" : { "M" : {                  "NonTrusted" : { "M" : {                      "WorkflowStatus" : { "S" : "NotifyReview" }                    }                  },                  "Trusted" : { "M" : {                      "WorkflowStatus" : { "S" : "NotifyReview" }                    }                  }                }              },              "BSM" : { "M" : {                  "NonTrusted" : { "M" : {                      "WorkflowStatus" : { "S" : "NotifyReview" }                    }                  },                  "Trusted" : { "M" : {                      "WorkflowStatus" : { "S" : "NotifyReview" }                    }                  }                }              },              "CLOSURES" : { "M" : {                  "NonTrusted" : { "M" : {                      "WorkflowStatus" : { "S" : "Notify" }                    }                  },                  "Trusted" : { "M" : {                      "WorkflowStatus" : { "S" : "Notify" }                    }                  }                }              },              "CORRIDOR" : { "M" : {                  "NonTrusted" : { "M" : {                      "WorkflowStatus" : { "S" : "Notify" }                    }                  },                  "Trusted" : { "M" : {                      "WorkflowStatus" : { "S" : "Notify" }                    }                  }                }              },              "COUNT" : { "M" : {                  "NonTrusted" : { "M" : {                      "WorkflowStatus" : { "S" : "Notify" }                    }                  },                  "Trusted" : { "M" : {                      "WorkflowStatus" : { "S" : "Notify" }                    }                  }                }              },              "CRASH" : { "M" : {                  "NonTrusted" : { "M" : {                      "WorkflowStatus" : { "S" : "NotifyReview" }                    }                  },                  "Trusted" : { "M" : {                      "WorkflowStatus" : { "S" : "NotifyReview" }                    }                  }                }              },              "DMS" : { "M" : {                  "NonTrusted" : { "M" : {                      "WorkflowStatus" : { "S" : "Notify" }                    }                  },                  "Trusted" : { "M" : {                      "WorkflowStatus" : { "S" : "Notify" }                    }                  }                }              },              "PIKALERT" : { "M" : {                  "NonTrusted" : { "M" : {                      "WorkflowStatus" : { "S" : "NotifyReview" }                    }                  },                  "Trusted" : { "M" : {                      "WorkflowStatus" : { "S" : "NotifyReview" }                    }                  }                }              },              "RWIS" : { "M" : {                  "NonTrusted" : { "M" : {                      "WorkflowStatus" : { "S" : "Notify" }                    }                  },                  "Trusted" : { "M" : {                      "WorkflowStatus" : { "S" : "Notify" }                    }                  }                }              },              "SPEED" : { "M" : {                  "NonTrusted" : { "M" : {                      "WorkflowStatus" : { "S" : "NotifyReview" }                    }                  },                  "Trusted" : { "M" : {                      "WorkflowStatus" : { "S" : "NotifyReview" }                    }                  }                }              },              "TIM" : { "M" : {                  "NonTrusted" : { "M" : {                      "WorkflowStatus" : { "S" : "NotifyReview" }                    }                  },                  "Trusted" : { "M" : {                      "WorkflowStatus" : { "S" : "NotifyReview" }                    }                  }                }              },              "VSL" : { "M" : {                  "NonTrusted" : { "M" : {                      "WorkflowStatus" : { "S" : "Notify" }                    }                  },                  "Trusted" : { "M" : {                      "WorkflowStatus" : { "S" : "Notify" }                    }                  }                }              }            }          },          "ListOfPOC" : { "L" : [              { "S" : "tony@neaeraconsulting.com" },              { "S" : "RKYoung@uwyo.edu" },              { "S" : "santosh.karla@reancloud.com" },              { "S" : "swarnadee.bapat@reancloud.com" }            ]          },          "UpdateDate" : { "S" : "08-06-2018" },          "UsagePolicyDesc" : { "S" : "<p>The Wyoming DOT is providing ongoing access to data generated by the Connected Vehicle Pilot deployment to support performance measurement and evaluation activities to a select group of explicitly approved individuals.  The CV Pilot is an ongoing research activity and includes access to rapidly evolving data sets and products. Wyoming DOT makes no claims, promises or guarantees about the accuracy, completeness, or adequacy of the contents of data and expressly disclaims liability for errors and omissions in the data.</p><p>Conducting research activities on Wyoming DOT CV pilot data and resources is restricted to authorized individuals for the purpose for which access was granted.  Further, users of the Wyoming CV Pilot data are expected to use good judgment and research practices. This includes but is not limited to:<li>Using CV Pilot data in a lawful and appropriate manner<li>Respecting the rights and privacy of others<li>Maintaining the CV Pilot data in an appropriate manner including accessing the Secure Data Commons through proper authentication<li>Including appropriate citations to Wyoming DOT&#39;s Connected Vehicle Pilot when using data or results derived from the data<li>No data or derived results from the Wyoming data shall be exported or removed from the SDC in anyway without the express approval of the Wyoming DOT CV Pilot</p>" }        }      }    }  }}
            }
        }
    )

@mock_s3
@mock_ses
@mock_dynamodb2
def run_auto_export(file_path):
    key = 'auto_export/test_type/test'
    conn = setup_raw_submissions()
    conn.upload_file(file_path, Origin_Bucket_Name, key)
    setup_dynamodb_table()
    event = {"Records": [{"Sns": {
        "Message": "{\"Records\":[{\"s3\":{\"bucket\":{\"name\":\"" + Origin_Bucket_Name + "\"}, \"object\":{\"key\":\"" + key + "\"}}}]}"}}]}
    lambda_function.lambda_handler(event, '')

@mock_s3
@mock_ses
@mock_dynamodb2
def test_auto_export():
    print('-----------------------TEST_AUTO_EXPORT--------------------------')
    try:
        run_auto_export('./tests/testFiles/test')
    except botocore.errorfactory.MessageRejected as e:
        assert True

    assert False