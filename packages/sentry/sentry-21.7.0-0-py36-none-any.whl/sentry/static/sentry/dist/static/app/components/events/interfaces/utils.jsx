Object.defineProperty(exports, "__esModule", { value: true });
exports.stackTracePlatformIcon = exports.parseAssembly = exports.getImageRange = exports.parseAddress = exports.formatAddress = exports.removeFilterMaskedEntries = exports.objectToSortedTupleArray = exports.getFullUrl = exports.stringifyQueryList = exports.getCurlCommand = exports.escapeQuotes = void 0;
var tslib_1 = require("tslib");
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var compact_1 = tslib_1.__importDefault(require("lodash/compact"));
var isString_1 = tslib_1.__importDefault(require("lodash/isString"));
var uniq_1 = tslib_1.__importDefault(require("lodash/uniq"));
var qs = tslib_1.__importStar(require("query-string"));
var constants_1 = require("app/constants");
var utils_1 = require("app/utils");
var fileExtension_1 = require("app/utils/fileExtension");
function escapeQuotes(v) {
    return v.replace(/\\/g, '\\\\').replace(/"/g, '\\"');
}
exports.escapeQuotes = escapeQuotes;
// TODO(dcramer): support cookies
function getCurlCommand(data) {
    var e_1, _a;
    var _b, _c, _d;
    var result = 'curl';
    if (utils_1.defined(data.method) && data.method !== 'GET') {
        result += ' \\\n -X ' + data.method;
    }
    // TODO(benvinegar): just gzip? what about deflate?
    var compressed = (_b = data.headers) === null || _b === void 0 ? void 0 : _b.find(function (h) { return h[0] === 'Accept-Encoding' && h[1].indexOf('gzip') !== -1; });
    if (compressed) {
        result += ' \\\n --compressed';
    }
    // sort headers
    var headers = (_d = (_c = data.headers) === null || _c === void 0 ? void 0 : _c.sort(function (a, b) {
        return a[0] === b[0] ? 0 : a[0] < b[0] ? -1 : 1;
    })) !== null && _d !== void 0 ? _d : [];
    try {
        for (var headers_1 = tslib_1.__values(headers), headers_1_1 = headers_1.next(); !headers_1_1.done; headers_1_1 = headers_1.next()) {
            var header = headers_1_1.value;
            result += ' \\\n -H "' + header[0] + ': ' + escapeQuotes(header[1] + '') + '"';
        }
    }
    catch (e_1_1) { e_1 = { error: e_1_1 }; }
    finally {
        try {
            if (headers_1_1 && !headers_1_1.done && (_a = headers_1.return)) _a.call(headers_1);
        }
        finally { if (e_1) throw e_1.error; }
    }
    if (utils_1.defined(data.data)) {
        switch (data.inferredContentType) {
            case 'application/json':
                result += ' \\\n --data "' + escapeQuotes(JSON.stringify(data.data)) + '"';
                break;
            case 'application/x-www-form-urlencoded':
                result +=
                    ' \\\n --data "' +
                        escapeQuotes(qs.stringify(data.data)) +
                        '"';
                break;
            default:
                if (isString_1.default(data.data)) {
                    result += ' \\\n --data "' + escapeQuotes(data.data) + '"';
                }
                else if (Object.keys(data.data).length === 0) {
                    // Do nothing with empty object data.
                }
                else {
                    Sentry.withScope(function (scope) {
                        scope.setExtra('data', data);
                        Sentry.captureException(new Error('Unknown event data'));
                    });
                }
        }
    }
    result += ' \\\n "' + getFullUrl(data) + '"';
    return result;
}
exports.getCurlCommand = getCurlCommand;
function stringifyQueryList(query) {
    var e_2, _a;
    if (isString_1.default(query)) {
        return query;
    }
    var queryObj = {};
    try {
        for (var query_1 = tslib_1.__values(query), query_1_1 = query_1.next(); !query_1_1.done; query_1_1 = query_1.next()) {
            var kv = query_1_1.value;
            if (kv !== null && kv.length === 2) {
                var _b = tslib_1.__read(kv, 2), key = _b[0], value = _b[1];
                if (value !== null) {
                    if (Array.isArray(queryObj[key])) {
                        queryObj[key].push(value);
                    }
                    else {
                        queryObj[key] = [value];
                    }
                }
            }
        }
    }
    catch (e_2_1) { e_2 = { error: e_2_1 }; }
    finally {
        try {
            if (query_1_1 && !query_1_1.done && (_a = query_1.return)) _a.call(query_1);
        }
        finally { if (e_2) throw e_2.error; }
    }
    return qs.stringify(queryObj);
}
exports.stringifyQueryList = stringifyQueryList;
function getFullUrl(data) {
    var _a;
    var fullUrl = data === null || data === void 0 ? void 0 : data.url;
    if (!fullUrl) {
        return fullUrl;
    }
    if ((_a = data === null || data === void 0 ? void 0 : data.query) === null || _a === void 0 ? void 0 : _a.length) {
        fullUrl += '?' + stringifyQueryList(data.query);
    }
    if (data.fragment) {
        fullUrl += '#' + data.fragment;
    }
    return fullUrl;
}
exports.getFullUrl = getFullUrl;
/**
 * Converts an object of body/querystring key/value pairs
 * into a tuple of [key, value] pairs, and sorts them.
 *
 * This handles the case for query strings that were decoded like so:
 *
 *   ?foo=bar&foo=baz => { foo: ['bar', 'baz'] }
 *
 * By converting them to [['foo', 'bar'], ['foo', 'baz']]
 */
function objectToSortedTupleArray(obj) {
    return Object.keys(obj)
        .reduce(function (out, k) {
        var val = obj[k];
        return out.concat(Array.isArray(val)
            ? val.map(function (v) { return [k, v]; }) // key has multiple values (array)
            : [[k, val]] // key has single value
        );
    }, [])
        .sort(function (_a, _b) {
        var _c = tslib_1.__read(_a, 2), keyA = _c[0], valA = _c[1];
        var _d = tslib_1.__read(_b, 2), keyB = _d[0], valB = _d[1];
        // if keys are identical, sort on value
        if (keyA === keyB) {
            return valA < valB ? -1 : 1;
        }
        return keyA < keyB ? -1 : 1;
    });
}
exports.objectToSortedTupleArray = objectToSortedTupleArray;
// for context summaries and avatars
function removeFilterMaskedEntries(rawData) {
    var e_3, _a;
    var cleanedData = {};
    try {
        for (var _b = tslib_1.__values(Object.getOwnPropertyNames(rawData)), _c = _b.next(); !_c.done; _c = _b.next()) {
            var key = _c.value;
            if (rawData[key] !== constants_1.FILTER_MASK) {
                cleanedData[key] = rawData[key];
            }
        }
    }
    catch (e_3_1) { e_3 = { error: e_3_1 }; }
    finally {
        try {
            if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
        }
        finally { if (e_3) throw e_3.error; }
    }
    return cleanedData;
}
exports.removeFilterMaskedEntries = removeFilterMaskedEntries;
function formatAddress(address, imageAddressLength) {
    return "0x" + address.toString(16).padStart(imageAddressLength !== null && imageAddressLength !== void 0 ? imageAddressLength : 0, '0');
}
exports.formatAddress = formatAddress;
function parseAddress(address) {
    if (!address) {
        return 0;
    }
    try {
        return parseInt(address, 16) || 0;
    }
    catch (_e) {
        return 0;
    }
}
exports.parseAddress = parseAddress;
function getImageRange(image) {
    // The start address is normalized to a `0x` prefixed hex string. The event
    // schema also allows ingesting plain numbers, but this is converted during
    // ingestion.
    var startAddress = parseAddress(image === null || image === void 0 ? void 0 : image.image_addr);
    // The image size is normalized to a regular number. However, it can also be
    // `null`, in which case we assume that it counts up to the next image.
    var endAddress = startAddress + ((image === null || image === void 0 ? void 0 : image.image_size) || 0);
    return [startAddress, endAddress];
}
exports.getImageRange = getImageRange;
function parseAssembly(assembly) {
    var name;
    var version;
    var culture;
    var publicKeyToken;
    var pieces = assembly ? assembly.split(',') : [];
    if (pieces.length === 4) {
        name = pieces[0];
        version = pieces[1].split('Version=')[1];
        culture = pieces[2].split('Culture=')[1];
        publicKeyToken = pieces[3].split('PublicKeyToken=')[1];
    }
    return { name: name, version: version, culture: culture, publicKeyToken: publicKeyToken };
}
exports.parseAssembly = parseAssembly;
function stackTracePlatformIcon(platform, frames) {
    var fileExtensions = uniq_1.default(compact_1.default(frames.map(function (frame) { var _a; return fileExtension_1.getFileExtension((_a = frame.filename) !== null && _a !== void 0 ? _a : ''); })));
    if (fileExtensions.length === 1) {
        var newPlatform = fileExtension_1.fileExtensionToPlatform(fileExtensions[0]);
        return newPlatform !== null && newPlatform !== void 0 ? newPlatform : platform;
    }
    return platform;
}
exports.stackTracePlatformIcon = stackTracePlatformIcon;
//# sourceMappingURL=utils.jsx.map