Object.defineProperty(exports, "__esModule", { value: true });
exports.isNativePlatform = void 0;
function isNativePlatform(platform) {
    switch (platform) {
        case 'cocoa':
        case 'objc':
        case 'native':
        case 'swift':
        case 'c':
            return true;
        default:
            return false;
    }
}
exports.isNativePlatform = isNativePlatform;
//# sourceMappingURL=platform.jsx.map