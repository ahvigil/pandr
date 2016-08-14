#!/usr/bin/env Rscript
# generate R data files for testing against
setwd('./tests/data')

dir.create('rds', showWarnings=F)
dir.create('rdata', showWarnings=F)

# Pretty much the simplest save possible
x <- 5
saveRDS(x, 'rds/x.bin', ascii=F, compress=F)
saveRDS(x, 'rds/x.bin.gz', ascii=F, compress='gzip')
saveRDS(x, 'rds/x.bin.bz2', ascii=F, compress='bzip2')
saveRDS(x, 'rds/x.bin.xz', ascii=F, compress='xz')
saveRDS(x, 'rds/x.txt', ascii=T, compress=F)
saveRDS(x, 'rds/x.txt.gz', ascii=T, compress='gzip')
saveRDS(x, 'rds/x.txt.bz2', ascii=T, compress='bzip2')
saveRDS(x, 'rds/x.txt.xz', ascii=T, compress='xz')
save(x, file='rdata/x.bin', ascii=F, compress=F)
save(x, file='rdata/x.bin.gz', ascii=F, compress='gzip')
save(x, file='rdata/x.bin.bz2', ascii=F, compress='bzip2')
save(x, file='rdata/x.bin.xz', ascii=F, compress='xz')
save(x, file='rdata/x.txt', ascii=T, compress=F)
save(x, file='rdata/x.txt.gz', ascii=T, compress='gzip')
save(x, file='rdata/x.txt.bz2', ascii=T, compress='bzip2')
save(x, file='rdata/x.txt.xz', ascii=T, compress='xz')

library(datasets)

for(dataset in ls('package:datasets')){
    data <- get(dataset)
    saveRDS(data, sprintf('rds/%s.bin', dataset), ascii=F, compress=F)
    saveRDS(data, sprintf('rds/%s.bin.gz', dataset), ascii=F, compress='gzip')
    saveRDS(data, sprintf('rds/%s.bin.bz2', dataset), ascii=F, compress='bzip2')
    saveRDS(data, sprintf('rds/%s.bin.xz', dataset), ascii=F, compress='xz')
    saveRDS(data, sprintf('rds/%s.txt', dataset), ascii=T, compress=F)
    saveRDS(data, sprintf('rds/%s.txt.gz', dataset), ascii=T, compress='gzip')
    saveRDS(data, sprintf('rds/%s.txt.bz2', dataset), ascii=T, compress='bzip2')
    saveRDS(data, sprintf('rds/%s.txt.xz', dataset), ascii=T, compress='xz')
    save(data, file=sprintf('rdata/%s.bin', dataset), ascii=F, compress=F)
    save(data, file=sprintf('rdata/%s.bin.gz', dataset), ascii=F, compress='gzip')
    save(data, file=sprintf('rdata/%s.bin.bz2', dataset), ascii=F, compress='bzip2')
    save(data, file=sprintf('rdata/%s.bin.xz', dataset), ascii=F, compress='xz')
    save(data, file=sprintf('rdata/%s.txt', dataset), ascii=T, compress=F)
    save(data, file=sprintf('rdata/%s.txt.gz', dataset), ascii=T, compress='gzip')
    save(data, file=sprintf('rdata/%s.txt.bz2', dataset), ascii=T, compress='bzip2')
    save(data, file=sprintf('rdata/%s.txt.xz', dataset), ascii=T, compress='xz')
}
