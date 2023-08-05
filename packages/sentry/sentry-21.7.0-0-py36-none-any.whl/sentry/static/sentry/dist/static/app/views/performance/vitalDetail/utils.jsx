var _a, _b, _c, _d, _e, _f, _g;
Object.defineProperty(exports, "__esModule", { value: true });
exports.getMaxOfSeries = exports.vitalAbbreviations = exports.vitalDescription = exports.vitalChartTitleMap = exports.vitalMap = exports.getVitalDetailTableMehStatusFunction = exports.getVitalDetailTablePoorStatusFunction = exports.vitalNameFromLocation = exports.vitalDetailRouteWithQuery = exports.vitalStateIcons = exports.vitalStateColors = exports.VitalState = exports.webVitalMeh = exports.webVitalPoor = exports.generateVitalDetailRoute = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var icons_1 = require("app/icons");
var fields_1 = require("app/utils/discover/fields");
var queryString_1 = require("app/utils/queryString");
function generateVitalDetailRoute(_a) {
    var orgSlug = _a.orgSlug;
    return "/organizations/" + orgSlug + "/performance/vitaldetail/";
}
exports.generateVitalDetailRoute = generateVitalDetailRoute;
exports.webVitalPoor = (_a = {},
    _a[fields_1.WebVital.FP] = 3000,
    _a[fields_1.WebVital.FCP] = 3000,
    _a[fields_1.WebVital.LCP] = 4000,
    _a[fields_1.WebVital.FID] = 300,
    _a[fields_1.WebVital.CLS] = 0.25,
    _a);
exports.webVitalMeh = (_b = {},
    _b[fields_1.WebVital.FP] = 1000,
    _b[fields_1.WebVital.FCP] = 1000,
    _b[fields_1.WebVital.LCP] = 2500,
    _b[fields_1.WebVital.FID] = 100,
    _b[fields_1.WebVital.CLS] = 0.1,
    _b);
var VitalState;
(function (VitalState) {
    VitalState["POOR"] = "Poor";
    VitalState["MEH"] = "Meh";
    VitalState["GOOD"] = "Good";
})(VitalState = exports.VitalState || (exports.VitalState = {}));
exports.vitalStateColors = (_c = {},
    _c[VitalState.POOR] = 'red300',
    _c[VitalState.MEH] = 'yellow300',
    _c[VitalState.GOOD] = 'green300',
    _c);
exports.vitalStateIcons = (_d = {},
    _d[VitalState.POOR] = <icons_1.IconFire color={exports.vitalStateColors[VitalState.POOR]}/>,
    _d[VitalState.MEH] = <icons_1.IconWarning color={exports.vitalStateColors[VitalState.MEH]}/>,
    _d[VitalState.GOOD] = (<icons_1.IconCheckmark color={exports.vitalStateColors[VitalState.GOOD]} isCircled/>),
    _d);
function vitalDetailRouteWithQuery(_a) {
    var orgSlug = _a.orgSlug, vitalName = _a.vitalName, projectID = _a.projectID, query = _a.query;
    var pathname = generateVitalDetailRoute({
        orgSlug: orgSlug,
    });
    return {
        pathname: pathname,
        query: {
            vitalName: vitalName,
            project: projectID,
            environment: query.environment,
            statsPeriod: query.statsPeriod,
            start: query.start,
            end: query.end,
            query: query.query,
        },
    };
}
exports.vitalDetailRouteWithQuery = vitalDetailRouteWithQuery;
function vitalNameFromLocation(location) {
    var _vitalName = queryString_1.decodeScalar(location.query.vitalName);
    var vitalName = Object.values(fields_1.WebVital).find(function (v) { return v === _vitalName; });
    if (vitalName) {
        return vitalName;
    }
    else {
        return fields_1.WebVital.LCP;
    }
}
exports.vitalNameFromLocation = vitalNameFromLocation;
function getVitalDetailTablePoorStatusFunction(vitalName) {
    var vitalThreshold = exports.webVitalPoor[vitalName];
    var statusFunction = "compare_numeric_aggregate(" + fields_1.getAggregateAlias("p75(" + vitalName + ")") + ",greater," + vitalThreshold + ")";
    return statusFunction;
}
exports.getVitalDetailTablePoorStatusFunction = getVitalDetailTablePoorStatusFunction;
function getVitalDetailTableMehStatusFunction(vitalName) {
    var vitalThreshold = exports.webVitalMeh[vitalName];
    var statusFunction = "compare_numeric_aggregate(" + fields_1.getAggregateAlias("p75(" + vitalName + ")") + ",greater," + vitalThreshold + ")";
    return statusFunction;
}
exports.getVitalDetailTableMehStatusFunction = getVitalDetailTableMehStatusFunction;
exports.vitalMap = (_e = {},
    _e[fields_1.WebVital.FCP] = 'First Contentful Paint',
    _e[fields_1.WebVital.CLS] = 'Cumulative Layout Shift',
    _e[fields_1.WebVital.FID] = 'First Input Delay',
    _e[fields_1.WebVital.LCP] = 'Largest Contentful Paint',
    _e);
exports.vitalChartTitleMap = exports.vitalMap;
exports.vitalDescription = (_f = {},
    _f[fields_1.WebVital.FCP] = 'First Contentful Paint (FCP) measures the amount of time the first content takes to render in the viewport. Like FP, this could also show up in any form from the document object model (DOM), such as images, SVGs, or text blocks.',
    _f[fields_1.WebVital.CLS] = 'Cumulative Layout Shift (CLS) is the sum of individual layout shift scores for every unexpected element shift during the rendering process. Imagine navigating to an article and trying to click a link before the page finishes loading. Before your cursor even gets there, the link may have shifted down due to an image rendering. Rather than using duration for this Web Vital, the CLS score represents the degree of disruptive and visually unstable shifts.',
    _f[fields_1.WebVital.FID] = 'First Input Delay measures the response time when the user tries to interact with the viewport. Actions maybe include clicking a button, link or other custom Javascript controller. It is key in helping the user determine if a page is usable or not.',
    _f[fields_1.WebVital.LCP] = 'Largest Contentful Paint (LCP) measures the render time for the largest content to appear in the viewport. This may be in any form from the document object model (DOM), such as images, SVGs, or text blocks. It’s the largest pixel area in the viewport, thus most visually defining. LCP helps developers understand how long it takes to see the main content on the page.',
    _f);
exports.vitalAbbreviations = (_g = {},
    _g[fields_1.WebVital.FCP] = 'FCP',
    _g[fields_1.WebVital.CLS] = 'CLS',
    _g[fields_1.WebVital.FID] = 'FID',
    _g[fields_1.WebVital.LCP] = 'LCP',
    _g);
function getMaxOfSeries(series) {
    var e_1, _a, e_2, _b;
    var max = -Infinity;
    try {
        for (var series_1 = tslib_1.__values(series), series_1_1 = series_1.next(); !series_1_1.done; series_1_1 = series_1.next()) {
            var data = series_1_1.value.data;
            try {
                for (var data_1 = (e_2 = void 0, tslib_1.__values(data)), data_1_1 = data_1.next(); !data_1_1.done; data_1_1 = data_1.next()) {
                    var point = data_1_1.value;
                    max = Math.max(max, point.value);
                }
            }
            catch (e_2_1) { e_2 = { error: e_2_1 }; }
            finally {
                try {
                    if (data_1_1 && !data_1_1.done && (_b = data_1.return)) _b.call(data_1);
                }
                finally { if (e_2) throw e_2.error; }
            }
        }
    }
    catch (e_1_1) { e_1 = { error: e_1_1 }; }
    finally {
        try {
            if (series_1_1 && !series_1_1.done && (_a = series_1.return)) _a.call(series_1);
        }
        finally { if (e_1) throw e_1.error; }
    }
    return max;
}
exports.getMaxOfSeries = getMaxOfSeries;
//# sourceMappingURL=utils.jsx.map