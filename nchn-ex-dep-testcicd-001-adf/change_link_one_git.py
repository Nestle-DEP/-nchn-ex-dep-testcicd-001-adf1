import os
import shutil
import sys
import json
import subprocess


# config path
def config(name, env, link, path):
    try:
        adfName = name
        releaseEnv = env
        keyVaultLink = link
        rootPath = path
    except Exception as e:
        print(e)
        print("=======================请输入参数==============")
    else:
        adfPreName = adfName.split('-')[0]
        adfNum = adfName.split('-')[1]


        if (adfPreName == 'dep'):
            adfName = adfNum
            dbPath = rootPath + "/db/{0}.json".format(adfName)
        else:
            dbPath = rootPath + "/db/{0}.json".format(adfPreName)

        armPath = rootPath
        masterArm = rootPath + "/ARMTemplateForFactory.json"
        dirsPath = rootPath + "/one/"

        # current don't need
        newArm = rootPath + "/yy_arm_template.json"
        azureShell = rootPath + "/CreateLinked.ps1"

    return newArm, masterArm, azureShell, adfPreName, adfNum, adfName, releaseEnv, keyVaultLink, dbPath, dirsPath, armPath


# if json data exists
def isExtend(data, tagkey):
    if (type(data) != type({})):
        print('please input a json!')
    else:
        key_list = data.keys()
        for key in key_list:
            if (key == tagkey):
                return True
    return False


# get env variable
def getEnvVariable(adfName, flag):
    if flag == 'st':
        DataLake_Secondary_value = "Ok5vOtwsgcYXFJZjcOr2OGcgXV1BhsIJkbj4/DW6mrCVEAt3013EtA75OQMdcw9QVg7y2LOZwFjm4N8zHv+cPw=="
        ir_path = "/subscriptions/3ac482b6-893e-4750-b5b8-0e94a3bd522c/resourcegroups/nchn-st-dep-dl-rgp/providers/Microsoft.DataFactory/factories/nchn-st-dep-001-adf/integrationruntimes/adf-ir"
        adf_ir_cnbei_preprod = "/subscriptions/3ac482b6-893e-4750-b5b8-0e94a3bd522c/resourcegroups/nchn-pr-dep-dl-rgp/providers/Microsoft.DataFactory/factories/nchn-pr-dep-001-adf/integrationruntimes/adf-ir-cnbei-prod"
        abfs = "abfs://stgdatalake@nchnstdep003sta.dfs.core.chinacloudapi.cn/preprod"
        sub_id = "3ac482b6-893e-4750-b5b8-0e94a3bd522c"
        fileSystem = "stgdatalake"
        dirpath = "preprod/"
        adfnames = "nchn-st-dep-{0}-adf".format(adfName)
    elif flag == 'ts':
        DataLake_Secondary_value = "djyoRCnIXhk1Erwmlr4Bc0pmrhgD5tqQqPaksNf2uslI8Vd01uZXQzBdqDwDZ0pYOPEZipmdlIYA8KMjxnKXwg=="
        ir_path = "/subscriptions/6d8d10a3-4fef-47a8-8cdc-a7b0443cdc44/resourcegroups/nchn-ts-dep-dl-rgp/providers/Microsoft.DataFactory/factories/nchn-ts-dep-001-adf/integrationruntimes/adf-ir"
        adf_ir_cnbei_preprod = "/subscriptions/6d8d10a3-4fef-47a8-8cdc-a7b0443cdc44/resourcegroups/nchn-dv-dep-dl-rgp/providers/Microsoft.DataFactory/factories/nchn-dv-dep-001-adf/integrationruntimes/adf-ir-cnbei-preprod"
        abfs = "abfs://tstdatalake@nchntsdep003sta.dfs.core.chinacloudapi.cn/test"
        sub_id = "6d8d10a3-4fef-47a8-8cdc-a7b0443cdc44"
        fileSystem = "tstdatalake"
        dirpath = "test/"
        adfnames = "nchn-ts-dep-{0}-adf".format(adfName)
    elif flag == 'dv':
        DataLake_Secondary_value = "Cle7AsUyBDJyynyfFimN4O8Alb/Uul1HXNV4xZbCwtPLf4UDqmUP1FCNQ5KaBkyVvRCc8Uu74JBUu4K2MYiiUQ=="
        ir_path = "/subscriptions/6d8d10a3-4fef-47a8-8cdc-a7b0443cdc44/resourcegroups/nchn-dv-dep-dl-rgp/providers/Microsoft.DataFactory/factories/nchn-dv-dep-001-adf/integrationruntimes/adf-ir-dv"
        adf_ir_cnbei_preprod = "/subscriptions/6d8d10a3-4fef-47a8-8cdc-a7b0443cdc44/resourcegroups/nchn-dv-dep-dl-rgp/providers/Microsoft.DataFactory/factories/nchn-dv-dep-001-adf/integrationruntimes/adf-ir-cnbei-preprod"
        abfs = "abfs://devdatalake@nchndvdep003sta.dfs.core.chinacloudapi.cn/dev"
        sub_id = "6d8d10a3-4fef-47a8-8cdc-a7b0443cdc44"
        fileSystem = "devdatalake"
        dirpath = "dev/"
        adfnames = "nchn-dv-dep-{0}-adf".format(adfName)
    elif flag == 'pr':
        DataLake_Secondary_value = "9btfEwir3+KClgmy+zb9M3u5IFkoF/fhcFPGWib0DbhHMhnOYnxub668erDQrv20PV02QC29hI7+49Il1FLlOw=="
        ir_path = "/subscriptions/3ac482b6-893e-4750-b5b8-0e94a3bd522c/resourcegroups/nchn-pr-dep-dl-rgp/providers/Microsoft.DataFactory/factories/nchn-pr-dep-001-adf/integrationruntimes/prd-ir"
        adf_ir_cnbei_preprod = "/subscriptions/3ac482b6-893e-4750-b5b8-0e94a3bd522c/resourcegroups/nchn-pr-dep-dl-rgp/providers/Microsoft.DataFactory/factories/nchn-pr-dep-001-adf/integrationruntimes/adf-ir-cnbei-prod"
        abfs = "abfs://prddatalake@nchnprdep003sta.dfs.core.chinacloudapi.cn/prod"
        sub_id = "3ac482b6-893e-4750-b5b8-0e94a3bd522c"
        fileSystem = "prddatalake"
        dirpath = "prod/"
        adfnames = "nchn-pr-dep-{0}-adf".format(adfName)
    elif flag == 'ex':
        DataLake_Secondary_value = "WSonX3zOn6Xbd5xoFa6Jp2QuSzp3hlLKjzuTscRmIgJfZgWer0HISKWvsfCf/WGx5d1RIn63OXRCacgNP4JJFw=="
        ir_path = "/subscriptions/738b238c-d18b-4b67-98e2-2d514fcaa6ee/resourcegroups/nchn-ex-dep-dl-rgp/providers/Microsoft.DataFactory/factories/nchn-ex-dep-001-adf/integrationruntimes/adf-ir"
        adf_ir_cnbei_preprod = "/subscriptions/3ac482b6-893e-4750-b5b8-0e94a3bd522c/resourcegroups/nchn-pr-dep-dl-rgp/providers/Microsoft.DataFactory/factories/nchn-pr-dep-001-adf/integrationruntimes/adf-ir-cnbei-prod"
        abfs = "abfs://expdatalake@nchnexdep003sta.dfs.core.chinacloudapi.cn/exp"
        sub_id = "738b238c-d18b-4b67-98e2-2d514fcaa6ee"
        fileSystem = "expdatalake"
        dirpath = "exp/"
        adfnames = "nchn-ex-dep-{0}-adf".format(adfName)
    paramsList = [DataLake_Secondary_value, ir_path, adf_ir_cnbei_preprod, abfs, sub_id, fileSystem, dirpath, adfnames]
    return paramsList


# read master template
def readMasterArm(masterArm, masterFile):
    with open(masterArm, 'r', encoding='utf-8') as file_message:
        read_old_message = json.loads(file_message.read())
        dict1 = read_old_message['parameters']
        for x in dict1:
            if x != 'factoryName' and x.find("trigger") < 0:
                filename1 = "ARMTemplateForFactory.json"
                a = "%s-%s" % (filename1, x)
                filename2 = "ARMTemplateParametersForFactory.json"
                b = "%s-%s" % (filename2, x)
                masterFile.append(a)
                masterFile.append(b)


# replace linkedServices
def replaceLinkedServices(armPath, dbPath, dirPath, envFlag, adfName, adfPreName, keyVaultLink, masterFile):
    if not os.path.exists(dirPath):
        os.mkdir(dirPath)
    else:
        shutil.rmtree(dirPath)
        os.mkdir(dirPath)

    # 遍历所有模版文件
    for root, dirs, files in os.walk(armPath):
        for f in files:
            oldpath = os.path.join(root, f)
            if f == "ARMTemplateForFactory.json" or f == "ARMTemplateParametersForFactory.json":
                print("==============" + f + "==============")
                with open(oldpath, 'r', encoding='utf-8') as file_message:
                    read_old_message = json.loads(file_message.read())
                    # 区分读取ADF名称
                    if f == "ARMTemplateParametersForFactory.json":
                        oldAbfs = read_old_message['parameters']['factoryName']["value"]
                    else:
                        oldAbfs = read_old_message['parameters']['factoryName']["defaultValue"]
                    # json.dumps(read_old_message['resources']['properties']["activities"]["typeProperties"]["scriptPath"])

                    # 根据上一步提取的名称，拆分出原环境flag
                    oldflag = str(oldAbfs).split("-")[1]
                    # 获取原环境所有环境变量
                    oldflags = getEnvVariable(adfName, oldflag)
                    oldAbfs = oldflags[3]
                    oldfileSystem = oldflags[5]
                    olddirpath = oldflags[6]

                    # 提取新环境所有环境变量
                    newflags = getEnvVariable(adfName, envFlag)
                    DataLake_Secondary_value = newflags[0]
                    ir_path = newflags[1]
                    adf_ir_cnbei = newflags[2]
                    newAbfs = newflags[3]
                    fileSystem = newflags[5]
                    dirpath = newflags[6]
                    newadfname = newflags[7]
                    data = {
                        'type': "secureString",
                        'metadata': "Secure string for 'accountKey' of 'DataLake_Secondary'",
                        'defaultValue': DataLake_Secondary_value
                    }
                    newPrimaryPath = "https://nchn{0}dep003sta.dfs.core.chinacloudapi.cn".format(envFlag)
                    newSecondaryPath = "https://nchn{0}dep004sta.dfs.core.chinacloudapi.cn".format(envFlag)
                    newHDI = "ha002-nchn-{0}-dep-hdi-int.azurehdinsight.cn".format(envFlag)

                    # 获取旧的DataLake_Secondary_value
                    if f == "ARMTemplateParametersForFactory.json":
                        filetype = "value"
                        read_old_message['parameters']['DataLake_Secondary_accountKey'][filetype] = DataLake_Secondary_value
                    else:
                        filetype = "defaultValue"
                        read_old_message['parameters']['DataLake_Secondary_accountKey'] = data
                    oldadfname = read_old_message['parameters']['factoryName'][filetype]

                    # 获取旧的properties
                    if f == "ARMTemplateParametersForFactory.json" or f == "ARMTemplateForFactory.json":
                        oldHDI = read_old_message['parameters']['HDI_Hadoop_Hive_properties_typeProperties_host'][filetype]
                        oldPrimaryPath = read_old_message['parameters']['DataLake_Primary_properties_typeProperties_url'][
                            filetype]
                        oldSecondaryPath = \
                        read_old_message['parameters']['DataLake_Secondary_properties_typeProperties_url'][
                            filetype]
                        read_old_message['parameters']['KeyVault_properties_typeProperties_baseUrl'][
                            filetype] = keyVaultLink
                        read_old_message['parameters']['HDI_Hadoop_properties_typeProperties_userName'][
                            filetype] = adfPreName
                        read_old_message['parameters']['adf-ir_properties_typeProperties_linkedInfo_resourceId'][
                            filetype] = ir_path
                        read_old_message['parameters']['adf-ir-cnbei_properties_typeProperties_linkedInfo_resourceId'][
                            filetype] = adf_ir_cnbei

                    a = "%s-%s" % (f, "HDI_Hadoop_Hive_properties_typeProperties_host")
                    if a in masterFile:
                        oldHDI = read_old_message['parameters']['HDI_Hadoop_Hive_properties_typeProperties_host'][
                            filetype]
                    a = "%s-%s" % (f, "DataLake_Primary_properties_typeProperties_url")
                    if a in masterFile:
                        oldPrimaryPath = \
                        read_old_message['parameters']['DataLake_Primary_properties_typeProperties_url'][
                            filetype]
                    a = "%s-%s" % (f, "DataLake_Secondary_properties_typeProperties_url")
                    if a in masterFile:
                        oldSecondaryPath = \
                            read_old_message['parameters']['DataLake_Secondary_properties_typeProperties_url'][
                                filetype]
                    a = "%s-%s" % (f, "KeyVault_properties_typeProperties_baseUrl")
                    if a in masterFile:
                        read_old_message['parameters']['KeyVault_properties_typeProperties_baseUrl'][
                            filetype] = keyVaultLink
                    a = "%s-%s" % (f, "HDI_Hadoop_Hive_properties_typeProperties_username")
                    if a in masterFile:
                        read_old_message['parameters']['HDI_Hadoop_Hive_properties_typeProperties_username'][
                            filetype] = adfPreName
                    a = "%s-%s" % (f, "HDI_Hadoop_properties_typeProperties_userName")
                    if a in masterFile:
                        read_old_message['parameters']['HDI_Hadoop_properties_typeProperties_userName'][
                            filetype] = adfPreName
                    a = "%s-%s" % (f, "adf-ir_properties_typeProperties_linkedInfo_resourceId")
                    if a in masterFile:
                        read_old_message['parameters']['adf-ir_properties_typeProperties_linkedInfo_resourceId'][
                            filetype] = ir_path
                    a = "%s-%s" % (f, "adf-ir-cnbei_properties_typeProperties_linkedInfo_resourceId")
                    if a in masterFile:
                        read_old_message['parameters']['adf-ir-cnbei_properties_typeProperties_linkedInfo_resourceId'][
                            filetype] = adf_ir_cnbei
                    str_db = envFlag
                    print(dbPath)
                    if f == "ARMTemplateParametersForFactory.json":
                        with open(dbPath, "r", encoding='utf-8') as dbfile:
                            dbfiles = json.loads(dbfile.read())
                            if (isExtend(dbfiles, str_db)):
                                list_db = dbfiles[str_db]
                                if bool(list_db):
                                    for i, vt in enumerate(list_db):
                                        dbstr = list_db[vt]
                                        read_old_message['parameters'][vt]["value"] = dbstr
                            else:
                                print("没有配置数据库")
                    str_message = str(read_old_message).replace(oldPrimaryPath, newPrimaryPath) \
                        .replace(oldSecondaryPath, newSecondaryPath) \
                        .replace(oldadfname, newadfname) \
                        .replace(oldAbfs, newAbfs) \
                        .replace(oldHDI, newHDI) \
                        .replace(oldfileSystem, fileSystem) \
                        .replace(olddirpath, dirpath)
                    newarmPath = dirPath + "%s" % f
                    with open(newarmPath, "w", encoding='utf-8') as f:
                        json.dump(eval(str_message), f)

                print("生成创建linkedserver脚本")


# generate azure upload file
def genAzureShell(adfPreName, adfName, flag, azureShell, dirPath):
    sourepath = "\"" + dirPath + "\""
    # socret1 = "https://nchndvdep001sta.blob.core.chinacloudapi.cn/adf-arm/dsccwyeth/?sv=2019-10-10&ss=b&srt=sco&sp=rwdlac&se=2021-01-31T17:41:36Z&st=2020-12-15T09:41:36Z&spr=https&sig=JcYScN2N23iuKMTZ1jMKN8KAkY0zxHUsdCcRncM%2Fqbw%3D"
    socret1 = "https://nchnexdep001sta.blob.core.chinacloudapi.cn/adf-arm/{0}/{1}/?sv=2020-08-04&st=2022-04-24T07%3A11%3A36Z&se=2023-04-25T07%3A11%3A00Z&sr=c&sp=racwdl&sig=IwFGFkNPa%2B5jVImw8q2cTBdri20Jxlrv%2F%2Fdzmil2JUA%3D".format(
        adfPreName, flag)
    socret2 = "\"" + socret1 + "\""
    sub_id = "\"" + getEnvVariable(adfName, flag)[4] + "\""
    storageName = "\"" + "nchn{0}dep001sta".format(flag) + "\""
    resourceName = "\"" + "nchn-{0}-dep-dl-rgp".format(flag) + "\""
    containerName = "\"" + "adf-arm" + "\""
    containerUri = "\"" + "https://nchnexdep001sta.blob.core.chinacloudapi.cn/adf-arm/%s/%s" % (
    adfPreName, flag) + "/dirs\""
    templateFile = "\"" + dirPath + "ArmTemplate_master.json" + "\""
    parameterFile = "\"" + dirPath + "ArmTemplateParameters_master.json" + "\""
    containerSasToken = "\"" + "?sv=2020-08-04&st=2022-04-24T07%3A11%3A36Z&se=2023-04-25T07%3A11%3A00Z&sr=c&sp=racwdl&sig=IwFGFkNPa%2B5jVImw8q2cTBdri20Jxlrv%2F%2Fdzmil2JUA%3D" + "\""
    AzResource = "New-AzResourceGroupDeployment -Name DeployLinkedTemplate -ResourceGroupName $resourceGroupName -TemplateFile $templateFile -containerUri $containerUri  -containerSasToken $containerSasToken -TemplateParameterFile $parameterFile -verbose"

    # 生成azure powershell发布脚本
    fileObject = open(azureShell, 'w')
    fileObject.write("$context = Get-AzSubscription -SubscriptionId %s \n" % (sub_id))
    fileObject.write("Set-AzContext $context \n")
    fileObject.write(".\\azcopy copy %s %s --recursive=true \n" % (sourepath, socret2))
    fileObject.write("$storageAccountName=%s \n" % (storageName))
    fileObject.write("$resourceGroupName=%s \n" % (resourceName))
    fileObject.write("$containerName=%s \n" % (containerName))
    fileObject.write("$containerUri=%s \n" % (containerUri))
    fileObject.write("$templateFile =%s \n" % (templateFile))
    fileObject.write("$parameterFile =%s \n" % (parameterFile))
    fileObject.write("$containerSasToken =%s \n" % (containerSasToken))
    fileObject.write(AzResource)
    fileObject.close()


def pushToGitRepo(name, env, link, rootPath, repo, token):
    parmas = config(name, env, link, rootPath)
    os.chdir(parmas[11])
    cmd1 = "git add ."
    ps = subprocess.Popen(cmd1, stdout=subprocess.PIPE)
    psReturn1 = ps.stdout.read()
    print(psReturn1)
    import datetime
    i = datetime.datetime.now()
    cmd2 = "git commit -m" + "\"" + parmas[5] + str(i.year) + str(i.month) + str(i.day) + str(i.hour) + str(i.minute) + " \""
    ps = subprocess.Popen(cmd2, stdout=subprocess.PIPE)
    psReturn2 = ps.stdout.read()
    print(psReturn2)
    cmd3 = "git push https://" + token + repo
    ps = subprocess.Popen(cmd3, stdout=subprocess.PIPE)
    psReturn3 = ps.stdout.read()
    print(psReturn3)


def genScriptCopyShell():
    pass


def changeLink(rootPath, name, env, link):
    # newArm, masterArm, azureShell, adfPreName, adfNum, adfName, releaseEnv, keyVaultLink, dbPath, dirsPath, armPath, repoPath
    parmas = config(name, env, link, rootPath)
    # master file
    masterFile = list()
    readMasterArm(parmas[1], masterFile)
    print(masterFile)
    # replace old link with new link
    replaceLinkedServices(parmas[10], parmas[8], parmas[9], env, parmas[5], parmas[3], parmas[7], masterFile)
    # generate azure powershell file
    # adfPreName, adfName, flag, azureShell, dirPath
    # genAzureShell(parmas[3], parmas[5], env, parmas[2], parmas[9])

if __name__ == '__main__':
    rootPath = sys.argv[1]
    name = sys.argv[2]
    env = sys.argv[3]
    link = sys.argv[4]
    changeLink(rootPath, name, env, link)
