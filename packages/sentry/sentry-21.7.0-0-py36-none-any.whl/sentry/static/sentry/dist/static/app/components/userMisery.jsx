Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var scoreBar_1 = tslib_1.__importDefault(require("app/components/scoreBar"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var chartPalette_1 = tslib_1.__importDefault(require("app/constants/chartPalette"));
var locale_1 = require("app/locale");
var utils_1 = require("app/utils");
function UserMisery(props) {
    var bars = props.bars, barHeight = props.barHeight, userMisery = props.userMisery, miseryLimit = props.miseryLimit, totalUsers = props.totalUsers, miserableUsers = props.miserableUsers;
    // User Misery will always be > 0 because of the maximum a posteriori estimate
    // and below 5% will always be an overestimation of the actual proportion
    // of miserable to total unique users. We are going to visualize it as
    // 0 User Misery while still preserving the actual value for sorting purposes.
    var adjustedMisery = userMisery > 0.05 ? userMisery : 0;
    var palette = new Array(bars).fill([chartPalette_1.default[0][0]]);
    var score = Math.round(adjustedMisery * palette.length);
    var title;
    if (utils_1.defined(miserableUsers) && utils_1.defined(totalUsers) && utils_1.defined(miseryLimit)) {
        title = locale_1.tct('[miserableUsers] out of [totalUsers] unique users waited more than [duration]ms', {
            miserableUsers: miserableUsers,
            totalUsers: totalUsers,
            duration: 4 * miseryLimit,
        });
    }
    else if (utils_1.defined(miseryLimit)) {
        title = locale_1.tct('User Misery score is [userMisery], representing users who waited more than more than [duration]ms.', {
            duration: 4 * miseryLimit,
            userMisery: userMisery.toFixed(3),
        });
    }
    else {
        title = locale_1.tct('User Misery score is [userMisery].', {
            userMisery: userMisery.toFixed(3),
        });
    }
    return (<tooltip_1.default title={title} containerDisplayMode="block">
      <scoreBar_1.default size={barHeight} score={score} palette={palette} radius={0}/>
    </tooltip_1.default>);
}
exports.default = UserMisery;
//# sourceMappingURL=userMisery.jsx.map