Object.defineProperty(exports, "__esModule", { value: true });
exports.snoozedDays = void 0;
var tslib_1 = require("tslib");
var moment_1 = tslib_1.__importDefault(require("moment"));
/**
 * Given a snoozed unix timestamp in seconds, returns the number of days since
 * the prompt was snoozed.
 *
 * @param snoozedTs Snoozed timestamp
 */
function snoozedDays(snoozedTs) {
    var now = moment_1.default.utc();
    var snoozedDay = moment_1.default.unix(snoozedTs).utc();
    return now.diff(snoozedDay, 'days');
}
exports.snoozedDays = snoozedDays;
//# sourceMappingURL=promptsActivity.jsx.map