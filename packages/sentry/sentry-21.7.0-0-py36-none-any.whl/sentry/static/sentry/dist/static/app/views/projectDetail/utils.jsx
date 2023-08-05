Object.defineProperty(exports, "__esModule", { value: true });
exports.didProjectOrEnvironmentChange = exports.shouldFetchPreviousPeriod = void 0;
var utils_1 = require("app/components/charts/utils");
function shouldFetchPreviousPeriod(datetime) {
    var start = datetime.start, end = datetime.end, period = datetime.period;
    return !start && !end && utils_1.canIncludePreviousPeriod(true, period);
}
exports.shouldFetchPreviousPeriod = shouldFetchPreviousPeriod;
function didProjectOrEnvironmentChange(location1, location2) {
    return (location1.query.environment !== location2.query.environment ||
        location1.query.project !== location2.query.project);
}
exports.didProjectOrEnvironmentChange = didProjectOrEnvironmentChange;
//# sourceMappingURL=utils.jsx.map