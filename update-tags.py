import csv, sys, argparse
from sys import path
path.append('helper')
path.append('C:/Users/cdang/Python/python3.5/packages')
from aws.tag import UpdateTag, IsTagExists
from ta.log import Log
from ta.services import GetB3ServiceName

#################################################
#                                               #
#            DEFINE VARIABLES                   #
#                                               #
#################################################

LogFileName = 'tagging.log'
CsvFileName = 'september.csv'
Overwrite = False

#################################################
#                                               #
#            DEFINE FUNCTIONS                   #
#                                               #
#################################################



#################################################
#                                               #
#            PROGRAM ENTRY                      #
#                                               #
#################################################

if __name__ == '__main__':

    ### exit if not python 3
    try:
        PyVerMin = (3,0)
        assert sys.version_info >= PyVerMin
    except Exception as e:
        print('You are using Python ' + sys.version[0] + ', but this program requires Python', PyVerMin[0])
        sys.exit()

    ### check command line arguments: --tag AwsTagName=CsvTagName
    parser = argparse.ArgumentParser()
    parser.add_argument('--tag', nargs=1, required=True, help='key/value pair of tag formatted as AwsTag=CsvTag, \
                        i.e. Channel=tag_channel or Capability=tag_capability')
    args = [i[1] for i in vars(parser.parse_args()).items()] #[[Channel=tag_channel]]
    tag = args[0][0] #Channel=tag_channel
    ### exit if tag value does not contain =
    if tag.find('=') != -1:
        AwsTagName, CsvTagName = tag.split('=')
    else:
        print('Value for --tag is incorrect. Check valid options using --help.')
        sys.exit()

    ### initialize local variable
    TagPropIndex = {CsvTagName: None, 'resource_id': None, 'service': None}

    ### initialize logging: Level can be INFO or DEBUG
    L = Log(Filename='tagging.log', Level='INFO')

    ### print starting divider
    L.TeeLog('----------------------------------------------------------')

    ### open csv file
    try:
        reader = open(CsvFileName, 'r')
        CsvReader = csv.reader(reader)
    except Exception as e:
        L.TeeLog("Failed to open file:", e)
        sys.exit()

    ### get tag properties index in first row
    try:
        for row in CsvReader:
            for K in TagPropIndex.keys():
                TagPropIndex[K] = row.index(K)
            break
    except Exception as e:
        L.TeeLog('Failed to get index:', e)
        sys.exit()

    ### counters
    RowCounter = 0
    UpdateSucceedCounter = 0
    UpdateFailedCounter = 0
    UpdateSkipCounter = 0

    ### continue to process csv file
    try:
        TagIdx = TagPropIndex[CsvTagName]
        ResourceIdx = TagPropIndex['resource_id']
        ServiceIdx = TagPropIndex['service']

        ### each row in csv
        for row in CsvReader:
            TagName = AwsTagName
            TagValue = row[TagIdx]
            ResourceId = row[ResourceIdx]
            Service = GetB3ServiceName(row[ServiceIdx])

            RowCounter += 1

            L.TeeLog('Tag #' + str(RowCounter) + ': ResourceId=' + str(ResourceId) + ' TagName='\
	                + str(TagName) + ' TagValue=' + str(TagValue) + ' Service=' + str(Service))

            ### skip if tag value is Unknown or None
            if TagValue.lower() == 'unknown' or TagValue.lower() == 'none':
                L.TeeLog('Skip update since tag equals None or Unknown')
                UpdateSkipCounter += 1
                continue

            ### skip s3 until issue resolved where tag update cleared all other tags
            #if Service == 's3':
            #    L.TeeLog('Skip service ' + Service + ' until issue resolved where tag update cleared all other tags')
            #    UpdateSkipCounter += 1
            #    continue

            ### skip if Overwrite is False and tag already exists
            try:
                if not Overwrite and IsTagExists(Service, ResourceId, TagName):
                    L.TeeLog('Skip update for ' + ResourceId + ' since tag ' + TagName + ' exists and Overwrite is ' \
                             + str(Overwrite))
                    UpdateSkipCounter += 1
                    continue
            except Exception as e:
                L.TeeLog('Skip update since we cannot verify whether tag name ' + TagName + ' exists: ' + str(e), 1)
                UpdateSkipCounter += 1
                continue

            ### update tag
            try:
                if UpdateTag(Service, ResourceId, TagName, TagValue):
                    L.TeeLog('Successfully updated resourceid=' + ResourceId)
                    UpdateSucceedCounter += 1
                else:
                    L.TeeLog('Failed to update resourceid=' + ResourceId)
                    UpdateFailedCounter += 1
            except Exception as e:
                L.TeeLog('Failed to update resourceid=' + ResourceId + ': ' + str(e))
                UpdateFailedCounter += 1
    except Exception as e:
        L.TeeLog('Error processing csv file:', e)
    finally:
        reader.close()

    ### print summary
    L.TeeLog('Summary: Total=' + str(RowCounter) + ' Successful=' + str(UpdateSucceedCounter) + ' Skip=' + \
            str(UpdateSkipCounter) + ' Failed=' + str(UpdateFailedCounter))

else:
    L.TeeLog('I\'m not a module.')
    sys.exit()
