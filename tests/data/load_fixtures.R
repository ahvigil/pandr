#!/usr/bin/env Rscript
# generate R data files for testing against
setwd('./tests/data')

dir.create('rds', showWarnings=F)
dir.create('rdata', showWarnings=F)
dir.create('types', showWarnings=F)

save_rds <- function(data, prefix){
    saveRDS(data, sprintf('%s.bin', prefix), ascii=F, compress=F)
    saveRDS(data, sprintf('%s.bin.gz', prefix), ascii=F, compress='gzip')
    saveRDS(data, sprintf('%s.bin.bz2', prefix), ascii=F, compress='bzip2')
    saveRDS(data, sprintf('%s.bin.xz', prefix), ascii=F, compress='xz')
    saveRDS(data, sprintf('%s.txt', prefix), ascii=T, compress=F)
    saveRDS(data, sprintf('%s.txt.gz', prefix), ascii=T, compress='gzip')
    saveRDS(data, sprintf('%s.txt.bz2', prefix), ascii=T, compress='bzip2')
    saveRDS(data, sprintf('%s.txt.xz', prefix), ascii=T, compress='xz')
}

save_rdata <- function(data, prefix){
    save(data, file=sprintf('%s.bin', prefix), ascii=F, compress=F)
    save(data, file=sprintf('%s.bin.gz', prefix), ascii=F, compress='gzip')
    save(data, file=sprintf('%s.bin.bz2', prefix), ascii=F, compress='bzip2')
    save(data, file=sprintf('%s.bin.xz', prefix), ascii=F, compress='xz')
    save(data, file=sprintf('%s.txt', prefix), ascii=T, compress=F)
    save(data, file=sprintf('%s.txt.gz', prefix), ascii=T, compress='gzip')
    save(data, file=sprintf('%s.txt.bz2', prefix), ascii=T, compress='bzip2')
    save(data, file=sprintf('%s.txt.xz', prefix), ascii=T, compress='xz')
}

# some basic types
save_rds(5, 'types/numeric')
save_rds(c(1,2,3,4,5), 'types/numeric_vec')
save_rds('test123', 'types/string')
save_rds(as.integer(c(1,2,3,4,5)), 'types/integer_vec')

library(datasets)

for(dataset in ls('package:datasets')){
    data <- get(dataset)
    save_rds(data, sprintf('rds/%s', dataset))
    save_rdata(data, sprintf('rds/%s', dataset))
}
