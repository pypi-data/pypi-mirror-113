Object.defineProperty(exports, "__esModule", { value: true });
exports.isSelectionEqual = exports.getDefaultSelection = exports.extractDatetimeSelectionParameters = exports.extractSelectionParameters = exports.getStateFromQuery = void 0;
var tslib_1 = require("tslib");
var identity_1 = tslib_1.__importDefault(require("lodash/identity"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var pick_1 = tslib_1.__importDefault(require("lodash/pick"));
var pickBy_1 = tslib_1.__importDefault(require("lodash/pickBy"));
var globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
var utils_1 = require("app/utils");
var dates_1 = require("app/utils/dates");
var getParams_1 = require("./getParams");
var DEFAULT_PARAMS = getParams_1.getParams({});
function getStateFromQuery(query, _a) {
    var _b = _a === void 0 ? {} : _a, _c = _b.allowEmptyPeriod, allowEmptyPeriod = _c === void 0 ? false : _c, _d = _b.allowAbsoluteDatetime, allowAbsoluteDatetime = _d === void 0 ? true : _d;
    var parsedParams = getParams_1.getParams(query, { allowEmptyPeriod: allowEmptyPeriod, allowAbsoluteDatetime: allowAbsoluteDatetime });
    var projectFromQuery = query[globalSelectionHeader_1.URL_PARAM.PROJECT];
    var environmentFromQuery = query[globalSelectionHeader_1.URL_PARAM.ENVIRONMENT];
    var period = parsedParams.statsPeriod;
    var utc = parsedParams.utc;
    var hasAbsolute = allowAbsoluteDatetime && !!parsedParams.start && !!parsedParams.end;
    var project;
    if (utils_1.defined(projectFromQuery) && Array.isArray(projectFromQuery)) {
        project = projectFromQuery.map(function (p) { return parseInt(p, 10); });
    }
    else if (utils_1.defined(projectFromQuery)) {
        var projectFromQueryIdInt = parseInt(projectFromQuery, 10);
        project = isNaN(projectFromQueryIdInt) ? [] : [projectFromQueryIdInt];
    }
    else {
        project = projectFromQuery;
    }
    var environment = utils_1.defined(environmentFromQuery) && !Array.isArray(environmentFromQuery)
        ? [environmentFromQuery]
        : environmentFromQuery;
    var start = hasAbsolute ? dates_1.getUtcToLocalDateObject(parsedParams.start) : null;
    var end = hasAbsolute ? dates_1.getUtcToLocalDateObject(parsedParams.end) : null;
    return {
        project: project,
        environment: environment,
        period: period || null,
        start: start || null,
        end: end || null,
        // params from URL will be a string
        utc: typeof utc !== 'undefined' ? utc === 'true' : null,
    };
}
exports.getStateFromQuery = getStateFromQuery;
/**
 * Extract the global selection parameters from an object
 * Useful for extracting global selection properties from the current URL
 * when building another URL.
 */
function extractSelectionParameters(query) {
    return pickBy_1.default(pick_1.default(query, Object.values(globalSelectionHeader_1.URL_PARAM)), identity_1.default);
}
exports.extractSelectionParameters = extractSelectionParameters;
/**
 * Extract the global selection datetime parameters from an object.
 */
function extractDatetimeSelectionParameters(query) {
    return pickBy_1.default(pick_1.default(query, Object.values(globalSelectionHeader_1.DATE_TIME_KEYS)), identity_1.default);
}
exports.extractDatetimeSelectionParameters = extractDatetimeSelectionParameters;
function getDefaultSelection() {
    var utc = DEFAULT_PARAMS.utc;
    return {
        projects: [],
        environments: [],
        datetime: {
            start: DEFAULT_PARAMS.start || null,
            end: DEFAULT_PARAMS.end || null,
            period: DEFAULT_PARAMS.statsPeriod || '',
            utc: typeof utc !== 'undefined' ? utc === 'true' : null,
        },
    };
}
exports.getDefaultSelection = getDefaultSelection;
/**
 * Compare the non-utc values of two selections.
 * Useful when re-fetching data based on globalselection changing.
 *
 * utc is not compared as there is a problem somewhere in the selection
 * data flow that results in it being undefined | null | boolean instead of null | boolean.
 * The additional undefined state makes this function just as unreliable as isEqual(selection, other)
 */
function isSelectionEqual(selection, other) {
    var _a, _b, _c, _d;
    if (!isEqual_1.default(selection.projects, other.projects) ||
        !isEqual_1.default(selection.environments, other.environments)) {
        return false;
    }
    // Use string comparison as we aren't interested in the identity of the datetimes.
    if (selection.datetime.period !== other.datetime.period ||
        ((_a = selection.datetime.start) === null || _a === void 0 ? void 0 : _a.toString()) !== ((_b = other.datetime.start) === null || _b === void 0 ? void 0 : _b.toString()) ||
        ((_c = selection.datetime.end) === null || _c === void 0 ? void 0 : _c.toString()) !== ((_d = other.datetime.end) === null || _d === void 0 ? void 0 : _d.toString())) {
        return false;
    }
    return true;
}
exports.isSelectionEqual = isSelectionEqual;
//# sourceMappingURL=utils.jsx.map