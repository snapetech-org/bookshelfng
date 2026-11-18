FROM mcr.microsoft.com/dotnet-buildtools/prereqs:azurelinux-3.0-net11.0-cross-x86@sha256:efd21070248f3e6cd728b069e6708de2a5188162bd3a7e2fe357732f4f78b848
RUN tdnf --refresh update -y && tdnf clean all
# Runtime pack compilation uses the cross sysroot and has no Azure CLI dependency.
RUN rpm -e azure-cli && clang --version && test -d /crossrootfs/x86
