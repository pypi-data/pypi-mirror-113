Object.defineProperty(exports, "__esModule", { value: true });
exports.decodeInteger = exports.decodeList = exports.decodeScalar = exports.appendTagCondition = exports.addQueryParamsToExistingUrl = exports.formatQueryString = void 0;
var tslib_1 = require("tslib");
var isString_1 = tslib_1.__importDefault(require("lodash/isString"));
var queryString = tslib_1.__importStar(require("query-string"));
var utils_1 = require("app/utils");
// remove leading and trailing whitespace and remove double spaces
function formatQueryString(qs) {
    return qs.trim().replace(/\s+/g, ' ');
}
exports.formatQueryString = formatQueryString;
function addQueryParamsToExistingUrl(origUrl, queryParams) {
    var url;
    try {
        url = new URL(origUrl);
    }
    catch (_a) {
        return '';
    }
    var searchEntries = url.searchParams.entries();
    // Order the query params alphabetically.
    // Otherwise ``queryString`` orders them randomly and it's impossible to test.
    var params = JSON.parse(JSON.stringify(queryParams));
    var query = tslib_1.__assign(tslib_1.__assign({}, Object.fromEntries(searchEntries)), params);
    return url.protocol + "//" + url.host + url.pathname + "?" + queryString.stringify(query);
}
exports.addQueryParamsToExistingUrl = addQueryParamsToExistingUrl;
/**
 * Append a tag key:value to a query string.
 *
 * Handles spacing and quoting if necessary.
 */
function appendTagCondition(query, key, value) {
    var currentQuery = Array.isArray(query) ? query.pop() : isString_1.default(query) ? query : '';
    if (typeof value === 'string' && /[:\s\(\)\\"]/g.test(value)) {
        value = "\"" + utils_1.escapeDoubleQuotes(value) + "\"";
    }
    if (currentQuery) {
        currentQuery += " " + key + ":" + value;
    }
    else {
        currentQuery = key + ":" + value;
    }
    return currentQuery;
}
exports.appendTagCondition = appendTagCondition;
function decodeScalar(value, fallback) {
    if (!value) {
        return fallback;
    }
    var unwrapped = Array.isArray(value) && value.length > 0
        ? value[0]
        : isString_1.default(value)
            ? value
            : fallback;
    return isString_1.default(unwrapped) ? unwrapped : fallback;
}
exports.decodeScalar = decodeScalar;
function decodeList(value) {
    if (!value) {
        return [];
    }
    return Array.isArray(value) ? value : isString_1.default(value) ? [value] : [];
}
exports.decodeList = decodeList;
function decodeInteger(value, fallback) {
    var unwrapped = decodeScalar(value);
    if (unwrapped === undefined) {
        return fallback;
    }
    var parsed = parseInt(unwrapped, 10);
    if (isFinite(parsed)) {
        return parsed;
    }
    return fallback;
}
exports.decodeInteger = decodeInteger;
exports.default = {
    decodeInteger: decodeInteger,
    decodeList: decodeList,
    decodeScalar: decodeScalar,
    formatQueryString: formatQueryString,
    addQueryParamsToExistingUrl: addQueryParamsToExistingUrl,
    appendTagCondition: appendTagCondition,
};
//# sourceMappingURL=queryString.jsx.map