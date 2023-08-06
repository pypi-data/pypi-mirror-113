#### USE #####

 ## crypter file encrypt  ##
 
  call = binencrypt.crypter(data,output_file)
  call.encrypt()
 
 ## crypter_V2 text decrypt only exec  ##
 
  call = binencrypt.crypter_V2(data)
  out = call.encrypt()
  print(out)
  callde = binencrypt.crypter_V2(data)
  oytde = callde.decrypt()
  exec(oytde)
  
  ' this out not print only exec '


