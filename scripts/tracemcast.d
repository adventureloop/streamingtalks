syscall:freebsd:setsockopt:entry 
/arg1 == 0 && arg2 == 12/
{
    x = (u_char *)copyin(arg3, arg4);
    printf("%s\n%x %x %x %x\t%x %x %x %x \n", execname,
        x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7]);
    printf("%d %d %d %d\t%d %d %d %d \n", 
        x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7]);
}
