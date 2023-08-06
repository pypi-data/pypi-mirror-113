import rpy2.robjects as ro

def primos_r(n):
    codigo_en_r = """
    n_primos <- function(n) {
        if (n >= 2) {
            x = seq(2, n)
            num_primos = c()
            for (i in seq(2, n)) {
                if (any(x == i)) {
                    num_primos = c(num_primos, i)
                    x = c(x[(x %% i) != 0], i)
                }
            }
            return(num_primos)
        }
        else {
            return("El valor introducido debe ser mayor a 2")
        }
    } 
    n_primos(n)
    """
    ro.r(codigo_en_r)

    funcion_r = ro.globalenv['n_primos']
    return funcion_r(n)

#print(primos_r(12))