Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var badgeDisplayName_1 = tslib_1.__importDefault(require("app/components/idBadge/badgeDisplayName"));
var baseBadge_1 = tslib_1.__importDefault(require("app/components/idBadge/baseBadge"));
var Badge = function (_a) {
    var _b = _a.hideOverflow, hideOverflow = _b === void 0 ? true : _b, team = _a.team, props = tslib_1.__rest(_a, ["hideOverflow", "team"]);
    return (<baseBadge_1.default data-test-id="team-badge" displayName={<badgeDisplayName_1.default hideOverflow={hideOverflow}>{"#" + team.slug}</badgeDisplayName_1.default>} team={team} {...props}/>);
};
exports.default = Badge;
//# sourceMappingURL=badge.jsx.map