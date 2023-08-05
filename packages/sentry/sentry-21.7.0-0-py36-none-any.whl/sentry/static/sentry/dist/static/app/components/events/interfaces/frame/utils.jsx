Object.defineProperty(exports, "__esModule", { value: true });
exports.isDotnet = exports.getFrameHint = exports.getPlatform = exports.trimPackage = void 0;
var types_1 = require("app/components/events/interfaces/types");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
function trimPackage(pkg) {
    var pieces = pkg.split(/^([a-z]:\\|\\\\)/i.test(pkg) ? '\\' : '/');
    var filename = pieces[pieces.length - 1] || pieces[pieces.length - 2] || pkg;
    return filename.replace(/\.(dylib|so|a|dll|exe)$/, '');
}
exports.trimPackage = trimPackage;
function getPlatform(dataPlatform, platform) {
    // prioritize the frame platform but fall back to the platform
    // of the stack trace / exception
    return dataPlatform || platform;
}
exports.getPlatform = getPlatform;
function getFrameHint(frame) {
    // returning [hintText, hintIcon]
    var symbolicatorStatus = frame.symbolicatorStatus;
    var func = frame.function || '<unknown>';
    // Custom color used to match adjacent text.
    var warningIcon = <icons_1.IconQuestion size="xs" color={'#2c45a8'}/>;
    var errorIcon = <icons_1.IconWarning size="xs" color="red300"/>;
    if (func.match(/^@objc\s/)) {
        return [locale_1.t('Objective-C -> Swift shim frame'), warningIcon];
    }
    if (func.match(/^__?hidden#\d+/)) {
        return [locale_1.t('Hidden function from bitcode build'), errorIcon];
    }
    if (!symbolicatorStatus && func === '<unknown>') {
        // Only render this if the event was not symbolicated.
        return [locale_1.t('No function name was supplied by the client SDK.'), warningIcon];
    }
    if (func === '<unknown>' ||
        (func === '<redacted>' && symbolicatorStatus === types_1.SymbolicatorStatus.MISSING_SYMBOL)) {
        switch (symbolicatorStatus) {
            case types_1.SymbolicatorStatus.MISSING_SYMBOL:
                return [locale_1.t('The symbol was not found within the debug file.'), warningIcon];
            case types_1.SymbolicatorStatus.UNKNOWN_IMAGE:
                return [locale_1.t('No image is specified for the address of the frame.'), warningIcon];
            case types_1.SymbolicatorStatus.MISSING:
                return [
                    locale_1.t('The debug file could not be retrieved from any of the sources.'),
                    errorIcon,
                ];
            case types_1.SymbolicatorStatus.MALFORMED:
                return [locale_1.t('The retrieved debug file could not be processed.'), errorIcon];
            default:
        }
    }
    if (func === '<redacted>') {
        return [locale_1.t('Unknown system frame. Usually from beta SDKs'), warningIcon];
    }
    return [null, null];
}
exports.getFrameHint = getFrameHint;
function isDotnet(platform) {
    // csharp platform represents .NET and can be F#, VB or any language targeting CLS (the Common Language Specification)
    return platform === 'csharp';
}
exports.isDotnet = isDotnet;
//# sourceMappingURL=utils.jsx.map