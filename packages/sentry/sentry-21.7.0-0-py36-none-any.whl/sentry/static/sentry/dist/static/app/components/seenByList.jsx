Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var classnames_1 = tslib_1.__importDefault(require("classnames"));
var moment_1 = tslib_1.__importDefault(require("moment"));
var avatarList_1 = tslib_1.__importDefault(require("app/components/avatar/avatarList"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var formatters_1 = require("app/utils/formatters");
var SeenByList = function (_a) {
    var _b = _a.avatarSize, avatarSize = _b === void 0 ? 28 : _b, _c = _a.seenBy, seenBy = _c === void 0 ? [] : _c, _d = _a.iconTooltip, iconTooltip = _d === void 0 ? locale_1.t('People who have viewed this') : _d, _e = _a.maxVisibleAvatars, maxVisibleAvatars = _e === void 0 ? 10 : _e, _f = _a.iconPosition, iconPosition = _f === void 0 ? 'left' : _f, className = _a.className;
    var activeUser = configStore_1.default.get('user');
    var displayUsers = seenBy.filter(function (user) { return activeUser.id !== user.id; });
    if (displayUsers.length === 0) {
        return null;
    }
    // Note className="seen-by" is required for responsive design
    return (<SeenByWrapper iconPosition={iconPosition} className={classnames_1.default('seen-by', className)}>
      <avatarList_1.default users={displayUsers} avatarSize={avatarSize} maxVisibleAvatars={maxVisibleAvatars} renderTooltip={function (user) { return (<react_1.Fragment>
            {formatters_1.userDisplayName(user)}
            <br />
            {moment_1.default(user.lastSeen).format('LL')}
          </react_1.Fragment>); }}/>
      <IconWrapper iconPosition={iconPosition}>
        <tooltip_1.default title={iconTooltip}>
          <icons_1.IconShow size="sm" color="gray200"/>
        </tooltip_1.default>
      </IconWrapper>
    </SeenByWrapper>);
};
var SeenByWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  margin-top: 15px;\n  float: right;\n  ", ";\n"], ["\n  display: flex;\n  margin-top: 15px;\n  float: right;\n  ", ";\n"])), function (p) { return (p.iconPosition === 'left' ? 'flex-direction: row-reverse' : ''); });
var IconWrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  background-color: transparent;\n  color: ", ";\n  height: 28px;\n  width: 24px;\n  line-height: 26px;\n  text-align: center;\n  padding-top: ", ";\n  ", ";\n"], ["\n  background-color: transparent;\n  color: ", ";\n  height: 28px;\n  width: 24px;\n  line-height: 26px;\n  text-align: center;\n  padding-top: ", ";\n  ", ";\n"])), function (p) { return p.theme.textColor; }, space_1.default(0.5), function (p) { return (p.iconPosition === 'left' ? 'margin-right: 10px' : ''); });
exports.default = SeenByList;
var templateObject_1, templateObject_2;
//# sourceMappingURL=seenByList.jsx.map