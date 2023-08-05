Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var pick_1 = tslib_1.__importDefault(require("lodash/pick"));
var moment_1 = tslib_1.__importDefault(require("moment"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var count_1 = tslib_1.__importDefault(require("app/components/count"));
var getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
var globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
var locale_1 = require("app/locale");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var utils_2 = require("../../utils");
var styles_1 = require("./styles");
var TotalCrashFreeUsers = /** @class */ (function (_super) {
    tslib_1.__extends(TotalCrashFreeUsers, _super);
    function TotalCrashFreeUsers() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.shouldReload = true;
        return _this;
    }
    TotalCrashFreeUsers.prototype.getEndpoints = function () {
        var _a = this.props, location = _a.location, organization = _a.organization, projectSlug = _a.projectSlug, version = _a.version;
        return [
            [
                'releaseStats',
                "/projects/" + organization.slug + "/" + projectSlug + "/releases/" + version + "/stats/",
                {
                    query: tslib_1.__assign(tslib_1.__assign({}, getParams_1.getParams(pick_1.default(location.query, [globalSelectionHeader_1.URL_PARAM.PROJECT, globalSelectionHeader_1.URL_PARAM.ENVIRONMENT]))), { type: 'sessions' }),
                },
            ],
        ];
    };
    TotalCrashFreeUsers.prototype.componentDidUpdate = function (prevProps) {
        if (prevProps.version !== this.props.version) {
            this.remountComponent();
        }
    };
    TotalCrashFreeUsers.prototype.renderLoading = function () {
        return this.renderBody();
    };
    TotalCrashFreeUsers.prototype.renderBody = function () {
        var _a;
        var crashFreeTimeBreakdown = (_a = this.state.releaseStats) === null || _a === void 0 ? void 0 : _a.usersBreakdown;
        if (!(crashFreeTimeBreakdown === null || crashFreeTimeBreakdown === void 0 ? void 0 : crashFreeTimeBreakdown.length)) {
            return null;
        }
        var timeline = crashFreeTimeBreakdown
            .map(function (_a, index, data) {
            var date = _a.date, crashFreeUsers = _a.crashFreeUsers, totalUsers = _a.totalUsers;
            // count number of crash free users from knowing percent and total
            var crashFreeUserCount = Math.round(((crashFreeUsers !== null && crashFreeUsers !== void 0 ? crashFreeUsers : 0) * totalUsers) / 100);
            // first item of timeline is release creation date, then we want to have relative date label
            var dateLabel = index === 0
                ? locale_1.t('Release created')
                : moment_1.default(data[0].date).from(date, true) + " " + locale_1.t('later');
            return { date: moment_1.default(date), dateLabel: dateLabel, crashFreeUsers: crashFreeUsers, crashFreeUserCount: crashFreeUserCount };
        })
            // remove those timeframes that are in the future
            .filter(function (item) { return item.date.isBefore(); })
            // we want timeline to go from bottom to up
            .reverse();
        if (!timeline.length) {
            return null;
        }
        return (<styles_1.Wrapper>
        <styles_1.SectionHeading>{locale_1.t('Total Crash Free Users')}</styles_1.SectionHeading>
        <Timeline>
          {timeline.map(function (row) { return (<Row key={row.date.toString()}>
              <InnerRow>
                <Text bold>{row.date.format('MMMM D')}</Text>
                <Text bold right>
                  <count_1.default value={row.crashFreeUserCount}/>{' '}
                  {locale_1.tn('user', 'users', row.crashFreeUserCount)}
                </Text>
              </InnerRow>
              <InnerRow>
                <Text>{row.dateLabel}</Text>
                <Text right>
                  {utils_1.defined(row.crashFreeUsers)
                    ? utils_2.displayCrashFreePercent(row.crashFreeUsers)
                    : '-'}
                </Text>
              </InnerRow>
            </Row>); })}
        </Timeline>
      </styles_1.Wrapper>);
    };
    return TotalCrashFreeUsers;
}(asyncComponent_1.default));
var Timeline = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  line-height: 1.2;\n"], ["\n  font-size: ", ";\n  line-height: 1.2;\n"])), function (p) { return p.theme.fontSizeMedium; });
var DOT_SIZE = 10;
var Row = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  border-left: 1px solid ", ";\n  padding-left: ", ";\n  padding-bottom: ", ";\n  margin-left: ", ";\n  position: relative;\n\n  &:before {\n    content: '';\n    width: ", "px;\n    height: ", "px;\n    border-radius: 100%;\n    background-color: ", ";\n    position: absolute;\n    top: 0;\n    left: -", "px;\n  }\n\n  &:last-child {\n    border-left: 0;\n  }\n"], ["\n  border-left: 1px solid ", ";\n  padding-left: ", ";\n  padding-bottom: ", ";\n  margin-left: ", ";\n  position: relative;\n\n  &:before {\n    content: '';\n    width: ", "px;\n    height: ", "px;\n    border-radius: 100%;\n    background-color: ", ";\n    position: absolute;\n    top: 0;\n    left: -", "px;\n  }\n\n  &:last-child {\n    border-left: 0;\n  }\n"])), function (p) { return p.theme.border; }, space_1.default(2), space_1.default(1), space_1.default(1), DOT_SIZE, DOT_SIZE, function (p) { return p.theme.purple300; }, Math.floor(DOT_SIZE / 2));
var InnerRow = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-column-gap: ", ";\n  grid-auto-flow: column;\n  grid-auto-columns: 1fr;\n\n  padding-bottom: ", ";\n"], ["\n  display: grid;\n  grid-column-gap: ", ";\n  grid-auto-flow: column;\n  grid-auto-columns: 1fr;\n\n  padding-bottom: ", ";\n"])), space_1.default(2), space_1.default(0.5));
var Text = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  text-align: ", ";\n  color: ", ";\n  padding-bottom: ", ";\n  ", ";\n"], ["\n  text-align: ", ";\n  color: ", ";\n  padding-bottom: ", ";\n  ", ";\n"])), function (p) { return (p.right ? 'right' : 'left'); }, function (p) { return (p.bold ? p.theme.textColor : p.theme.gray300); }, space_1.default(0.25), overflowEllipsis_1.default);
exports.default = TotalCrashFreeUsers;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=totalCrashFreeUsers.jsx.map