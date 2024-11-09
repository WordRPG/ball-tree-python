""" 
    function projectPointOntoLine(A, B, C) {
    // Step 1: Compute the vector AB
    let AB = B.map((b, i) => b - A[i]);

    // Step 2: Compute the vector AC
    let AC = C.map((c, i) => c - A[i]);

    // Step 3: Compute the dot products
    let AB_dot_AB = AB.reduce((sum, ab) => sum + ab * ab, 0);
    let AC_dot_AB = AC.reduce((sum, ac, i) => sum + ac * AB[i], 0);

    // Step 4: Find the scalar projection of AC onto AB
    let scalarProjection = AC_dot_AB / AB_dot_AB;

    // Step 5: Calculate P by adding the scaled AB vector to A
    let P = A.map((a, i) => a + scalarProjection * AB[i]);

    return P;
}
""" 

def project_to_line(A, B, C): 
    AB = [B[i] - A[i] for i in range(len(A))]
    AC = [C[i] - A[i] for i in range(len(C))]
    AB_dot_AB = sum(x * x for x in AB) 
    AC_dot_AB = sum(AC[i] * AB[i] for i in range(len(AC))) 
    scalar = AC_dot_AB / AB_dot_AB 
    P = [A[i] + scalar * AB[i] for i in range(len(A))]
    return P