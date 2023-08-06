# Citrix ADC AWS AMI finder

This python package is used to find the latest AWS AMI for Citrix ADC products

## Usage

```bash
adcami -r REGION -p ADC_PRODUCT_NAME -v ADC_PRODUCT_VERSION
```

where (check [allowed values](#allowed-values))

* `-r | --region` : AWS Region from which AMI is available
  * OPTIONAL: If not given, the region in the default AWS-CLI config is taken
* `-p | --product` : Citrix Product Name
  * (default: `Citrix ADC VPX - Customer Licensed`)
* `-v | --version` : Citrix Product Version
  * (default: `13.0`)

### Pre-requisite

1. pip install adcami
2. [AWSCLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
3. [AWSCLI Configuration](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)

## Allowed Values

### Allowed Values for `-r` (enclose it in quotes)

* Citrix ADC VPX - Customer Licensed
* Citrix ADC VPX Express - 20 Mbps
* Citrix ADC VPX Standard Edition - 10 Mbps
* Citrix ADC VPX Standard Edition - 200 Mbps
* Citrix ADC VPX Standard Edition - 1000 Mbps
* Citrix ADC VPX Standard Edition - 3Gbps
* Citrix ADC VPX Standard Edition - 5Gbps
* Citrix ADC VPX Premium Edition - 10 Mbps
* Citrix ADC VPX Premium Edition - 200 Mbps
* Citrix ADC VPX Premium Edition - 1000 Mbps
* Citrix ADC VPX Premium Edition - 3Gbps
* Citrix ADC VPX Premium Edition - 5Gbps
* Citrix ADC VPX Advanced Edition - 10 Mbps
* Citrix ADC VPX Advanced Edition - 200 Mbps
* Citrix ADC VPX Advanced Edition - 1000 Mbps
* Citrix ADC VPX Advanced Edition - 3Gbps
* Citrix ADC VPX Advanced Edition - 5Gbps

### Allowed Values for `-p` (enclose it in quotes)

* 13.0
