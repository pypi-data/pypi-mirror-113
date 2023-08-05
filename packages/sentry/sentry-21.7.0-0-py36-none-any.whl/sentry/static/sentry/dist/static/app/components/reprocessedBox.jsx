Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var styles_1 = require("app/components/events/styles");
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var localStorage_1 = tslib_1.__importDefault(require("app/utils/localStorage"));
var ReprocessedBox = /** @class */ (function (_super) {
    tslib_1.__extends(ReprocessedBox, _super);
    function ReprocessedBox() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isBannerHidden: localStorage_1.default.getItem(_this.getBannerUniqueId()) === 'true',
        };
        _this.handleBannerDismiss = function () {
            localStorage_1.default.setItem(_this.getBannerUniqueId(), 'true');
            _this.setState({ isBannerHidden: true });
        };
        return _this;
    }
    ReprocessedBox.prototype.getBannerUniqueId = function () {
        var reprocessActivity = this.props.reprocessActivity;
        var id = reprocessActivity.id;
        return "reprocessed-activity-" + id + "-banner-dismissed";
    };
    ReprocessedBox.prototype.renderMessage = function () {
        var _a = this.props, orgSlug = _a.orgSlug, reprocessActivity = _a.reprocessActivity, groupCount = _a.groupCount, groupId = _a.groupId;
        var data = reprocessActivity.data;
        var eventCount = data.eventCount, oldGroupId = data.oldGroupId, newGroupId = data.newGroupId;
        var reprocessedEventsRoute = "/organizations/" + orgSlug + "/issues/?query=reprocessing.original_issue_id:" + oldGroupId;
        if (groupCount === 0) {
            return locale_1.tct('All events in this issue were moved during reprocessing. [link]', {
                link: (<link_1.default to={reprocessedEventsRoute}>
            {locale_1.tn('See %s new event', 'See %s new events', eventCount)}
          </link_1.default>),
            });
        }
        return locale_1.tct('Events in this issue were successfully reprocessed. [link]', {
            link: (<link_1.default to={reprocessedEventsRoute}>
          {newGroupId === Number(groupId)
                    ? locale_1.tn('See %s reprocessed event', 'See %s reprocessed events', eventCount)
                    : locale_1.tn('See %s new event', 'See %s new events', eventCount)}
        </link_1.default>),
        });
    };
    ReprocessedBox.prototype.render = function () {
        var isBannerHidden = this.state.isBannerHidden;
        if (isBannerHidden) {
            return null;
        }
        var className = this.props.className;
        return (<styles_1.BannerContainer priority="success" className={className}>
        <StyledBannerSummary>
          <icons_1.IconCheckmark color="green300" isCircled/>
          <span>{this.renderMessage()}</span>
          <StyledIconClose color="green300" aria-label={locale_1.t('Dismiss')} isCircled onClick={this.handleBannerDismiss}/>
        </StyledBannerSummary>
      </styles_1.BannerContainer>);
    };
    return ReprocessedBox;
}(react_1.Component));
exports.default = ReprocessedBox;
var StyledBannerSummary = styled_1.default(styles_1.BannerSummary)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  & > svg:last-child {\n    margin-right: 0;\n    margin-left: ", ";\n  }\n"], ["\n  & > svg:last-child {\n    margin-right: 0;\n    margin-left: ", ";\n  }\n"])), space_1.default(1));
var StyledIconClose = styled_1.default(icons_1.IconClose)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  cursor: pointer;\n"], ["\n  cursor: pointer;\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=reprocessedBox.jsx.map