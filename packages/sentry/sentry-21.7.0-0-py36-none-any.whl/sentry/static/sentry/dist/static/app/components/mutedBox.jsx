Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var dateTime_1 = tslib_1.__importDefault(require("app/components/dateTime"));
var duration_1 = tslib_1.__importDefault(require("app/components/duration"));
var styles_1 = require("app/components/events/styles");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var MutedBox = /** @class */ (function (_super) {
    tslib_1.__extends(MutedBox, _super);
    function MutedBox() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.renderReason = function () {
            var _a = _this.props.statusDetails, ignoreUntil = _a.ignoreUntil, ignoreCount = _a.ignoreCount, ignoreWindow = _a.ignoreWindow, ignoreUserCount = _a.ignoreUserCount, ignoreUserWindow = _a.ignoreUserWindow;
            if (ignoreUntil) {
                return locale_1.t('This issue has been ignored until %s', <strong>
          <dateTime_1.default date={ignoreUntil}/>
        </strong>);
            }
            else if (ignoreCount && ignoreWindow) {
                return locale_1.t('This issue has been ignored until it occurs %s time(s) in %s', <strong>{ignoreCount.toLocaleString()}</strong>, <strong>
          <duration_1.default seconds={ignoreWindow * 60}/>
        </strong>);
            }
            else if (ignoreCount) {
                return locale_1.t('This issue has been ignored until it occurs %s more time(s)', <strong>{ignoreCount.toLocaleString()}</strong>);
            }
            else if (ignoreUserCount && ignoreUserWindow) {
                return locale_1.t('This issue has been ignored until it affects %s user(s) in %s', <strong>{ignoreUserCount.toLocaleString()}</strong>, <strong>
          <duration_1.default seconds={ignoreUserWindow * 60}/>
        </strong>);
            }
            else if (ignoreUserCount) {
                return locale_1.t('This issue has been ignored until it affects %s more user(s)', <strong>{ignoreUserCount.toLocaleString()}</strong>);
            }
            return locale_1.t('This issue has been ignored');
        };
        _this.render = function () { return (<styles_1.BannerContainer priority="default">
      <styles_1.BannerSummary>
        <icons_1.IconMute color="red300" size="sm"/>
        <span>
          {_this.renderReason()}&nbsp;&mdash;&nbsp;
          {locale_1.t('You will not be notified of any changes and it will not show up by default in feeds.')}
        </span>
      </styles_1.BannerSummary>
    </styles_1.BannerContainer>); };
        return _this;
    }
    return MutedBox;
}(react_1.PureComponent));
exports.default = MutedBox;
//# sourceMappingURL=mutedBox.jsx.map