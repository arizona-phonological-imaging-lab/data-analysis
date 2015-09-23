
function(formula, type = NULL, data = list(), weights, subset, 
    offset, na.action = na.omit, partial = NULL, method = "v", 
    alpha = 1.4, varht = 1, id.basis = NULL, nbasis = NULL, seed = NULL, 
    random = NULL, skip.iter = FALSE) 
{
    mf <- match.call()
    mf$type <- mf$method <- mf$varht <- mf$partial <- NULL
    mf$alpha <- mf$id.basis <- mf$nbasis <- mf$seed <- NULL
    mf$random <- mf$skip.iter <- NULL
    mf[[1]] <- as.name("model.frame")
    mf <- eval(mf, parent.frame())
    wt <- model.weights(mf)
    nobs <- dim(mf)[1]
    if (is.null(id.basis)) {
        if (is.null(nbasis)) 
            nbasis <- max(30, ceiling(10 * nobs^(2/9)))
        if (nbasis >= nobs) 
            nbasis <- nobs
        if (!is.null(seed)) 
            set.seed(seed)
        id.basis <- sample(nobs, nbasis, prob = wt)
    }
    else {
        if (max(id.basis) > nobs | min(id.basis) < 1) 
            stop("gss error in ssanova: id.basis out of range")
        nbasis <- length(id.basis)
    }
    term <- mkterm(mf, type)
    if (!is.null(random)) {
        if (class(random) == "formula") 
            random <- mkran(random, data)
    }
    s <- r <- NULL
    nq <- 0
    for (label in term$labels) {
        if (label == "1") {
            s <- cbind(s, rep(1, len = nobs))
            next
        }
        x <- mf[, term[[label]]$vlist]
        x.basis <- mf[id.basis, term[[label]]$vlist]
        nphi <- term[[label]]$nphi
        nrk <- term[[label]]$nrk
        if (nphi) {
            phi <- term[[label]]$phi
            for (i in 1:nphi) s <- cbind(s, phi$fun(x, nu = i, 
                env = phi$env))
        }
        if (nrk) {
            rk <- term[[label]]$rk
            for (i in 1:nrk) {
                nq <- nq + 1
                r <- array(c(r, rk$fun(x, x.basis, nu = i, env = rk$env, 
                  out = TRUE)), c(nobs, nbasis, nq))
            }
        }
    }
    if (is.null(r)) 
        stop("gss error in ssanova: use lm for models with only unpenalized terms")
    if (!is.null(partial)) {
        mf.p <- model.frame(partial, data)
        for (lab in colnames(mf.p)) mf[, lab] <- mf.p[, lab]
        mt.p <- attr(mf.p, "terms")
        lab.p <- labels(mt.p)
        matx.p <- model.matrix(mt.p, data)[, -1, drop = FALSE]
        if (dim(matx.p)[1] != dim(mf)[1]) 
            stop("gss error in ssanova: partial data are of wrong size")
        matx.p <- scale(matx.p)
        center.p <- attr(matx.p, "scaled:center")
        scale.p <- attr(matx.p, "scaled:scale")
        s <- cbind(s, matx.p)
        part <- list(mt = mt.p, center = center.p, scale = scale.p)
    }
    else part <- lab.p <- NULL
    if (qr(s)$rank < dim(s)[2]) 
        stop("gss error in ssanova: unpenalized terms are linearly dependent")
    y <- model.response(mf, "numeric")
    offset <- model.offset(mf)
    if (!is.null(offset)) {
        term$labels <- c(term$labels, "offset")
        term$offset <- list(nphi = 0, nrk = 0)
        y <- y - offset
    }
    if (!is.null(wt)) 
        wt <- sqrt(wt)
    if (nq == 1) {
        r <- r[, , 1]
        z <- sspreg1(s, r, r[id.basis, ], y, wt, method, alpha, 
            varht, random)
    }
    else z <- mspreg1(s, r, id.basis, y, wt, method, alpha, varht, 
        random, skip.iter)
    desc <- NULL
    for (label in term$labels) desc <- rbind(desc, as.numeric(c(term[[label]][c("nphi", 
        "nrk")])))
    if (!is.null(partial)) {
        desc <- rbind(desc, matrix(c(1, 0), length(lab.p), 2, 
            byrow = TRUE))
    }
    desc <- rbind(desc, apply(desc, 2, sum))
    if (is.null(partial)) 
        rownames(desc) <- c(term$labels, "total")
    else rownames(desc) <- c(term$labels, lab.p, "total")
    colnames(desc) <- c("Unpenalized", "Penalized")
    obj <- c(list(call = match.call(), mf = mf, terms = term, 
        desc = desc, alpha = alpha, id.basis = id.basis, partial = part, 
        lab.p = lab.p, random = random, skip.iter = skip.iter), 
        z)
    class(obj) <- c("ssanova")
    obj
}

# 
# filePath <- '/home/josh/git/Autotrace/under-development/analysis/ssanova/minimal_working_examples/ssanova_ready_achlais.txt'
# 
# mydata <- read.table(filePath,h=T)
# 
# fit<-ssanova(Y~word*X,data=mydata)
