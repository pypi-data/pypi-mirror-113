Object.defineProperty(exports, "__esModule", { value: true });
exports.ErrorRobot = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var sentry_robot_png_1 = tslib_1.__importDefault(require("sentry-images/spot/sentry-robot.png"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var createSampleEventButton_1 = tslib_1.__importDefault(require("app/views/onboarding/createSampleEventButton"));
var ErrorRobot = /** @class */ (function (_super) {
    tslib_1.__extends(ErrorRobot, _super);
    function ErrorRobot() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            error: false,
            loading: false,
            sampleIssueId: _this.props.sampleIssueId,
        };
        return _this;
    }
    ErrorRobot.prototype.componentDidMount = function () {
        this.fetchData();
    };
    ErrorRobot.prototype.fetchData = function () {
        var _a, _b;
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _c, org, project, sampleIssueId, url, data, err_1, error;
            return tslib_1.__generator(this, function (_d) {
                switch (_d.label) {
                    case 0:
                        _c = this.props, org = _c.org, project = _c.project;
                        sampleIssueId = this.state.sampleIssueId;
                        if (!project) {
                            return [2 /*return*/];
                        }
                        if (utils_1.defined(sampleIssueId)) {
                            return [2 /*return*/];
                        }
                        url = "/projects/" + org.slug + "/" + project.slug + "/issues/";
                        this.setState({ loading: true });
                        _d.label = 1;
                    case 1:
                        _d.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.props.api.requestPromise(url, {
                                method: 'GET',
                                data: { limit: 1 },
                            })];
                    case 2:
                        data = _d.sent();
                        this.setState({ sampleIssueId: (data.length > 0 && data[0].id) || '' });
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _d.sent();
                        error = (_b = (_a = err_1 === null || err_1 === void 0 ? void 0 : err_1.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) !== null && _b !== void 0 ? _b : true;
                        this.setState({ error: error });
                        return [3 /*break*/, 4];
                    case 4:
                        this.setState({ loading: false });
                        return [2 /*return*/];
                }
            });
        });
    };
    ErrorRobot.prototype.render = function () {
        var _a = this.state, loading = _a.loading, error = _a.error, sampleIssueId = _a.sampleIssueId;
        var _b = this.props, org = _b.org, project = _b.project, gradient = _b.gradient;
        var sampleLink = project && (loading || error ? null : sampleIssueId) ? (<p>
          <react_router_1.Link to={"/" + org.slug + "/" + project.slug + "/issues/" + sampleIssueId + "/?sample"}>
            {locale_1.t('Or see your sample event')}
          </react_router_1.Link>
        </p>) : (<p>
          <createSampleEventButton_1.default priority="link" project={project} source="issues_list" disabled={!project} title={!project ? locale_1.t('Select a project to create a sample event') : undefined}>
            {locale_1.t('Create a sample event')}
          </createSampleEventButton_1.default>
        </p>);
        return (<ErrorRobotWrapper data-test-id="awaiting-events" className="awaiting-events" gradient={gradient}>
        <Robot aria-hidden>
          <Eye />
        </Robot>
        <MessageContainer>
          <h3>{locale_1.t('Waiting for events…')}</h3>
          <p>
            {locale_1.tct('Our error robot is waiting to [strike:devour] receive your first event.', {
                strike: <Strikethrough />,
            })}
          </p>
          <p>
            {project && (<button_1.default data-test-id="install-instructions" priority="primary" to={"/" + org.slug + "/" + project.slug + "/getting-started/" + (project.platform || '')}>
                {locale_1.t('Installation Instructions')}
              </button_1.default>)}
          </p>
          {sampleLink}
        </MessageContainer>
      </ErrorRobotWrapper>);
    };
    return ErrorRobot;
}(react_1.Component));
exports.ErrorRobot = ErrorRobot;
exports.default = withApi_1.default(ErrorRobot);
var ErrorRobotWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: center;\n  font-size: ", ";\n  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.08);\n  border-radius: 0 0 3px 3px;\n  padding: 40px ", " ", ";\n  min-height: 260px;\n\n  @media (max-width: ", ") {\n    flex-direction: column;\n    align-items: center;\n    padding: ", ";\n    text-align: center;\n  }\n"], ["\n  display: flex;\n  justify-content: center;\n  font-size: ", ";\n  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.08);\n  border-radius: 0 0 3px 3px;\n  padding: 40px ", " ", ";\n  min-height: 260px;\n\n  @media (max-width: ", ") {\n    flex-direction: column;\n    align-items: center;\n    padding: ", ";\n    text-align: center;\n  }\n"])), function (p) { return p.theme.fontSizeExtraLarge; }, space_1.default(3), space_1.default(3), function (p) { return p.theme.breakpoints[0]; }, space_1.default(3));
var Robot = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: block;\n  position: relative;\n  width: 220px;\n  height: 260px;\n  background: url(", ");\n  background-size: cover;\n\n  @media (max-width: ", ") {\n    width: 110px;\n    height: 130px;\n  }\n"], ["\n  display: block;\n  position: relative;\n  width: 220px;\n  height: 260px;\n  background: url(", ");\n  background-size: cover;\n\n  @media (max-width: ", ") {\n    width: 110px;\n    height: 130px;\n  }\n"])), sentry_robot_png_1.default, function (p) { return p.theme.breakpoints[0]; });
var Eye = styled_1.default('span')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  width: 12px;\n  height: 12px;\n  border-radius: 50%;\n  position: absolute;\n  top: 70px;\n  left: 81px;\n  transform: translateZ(0);\n  animation: blink-eye 0.6s infinite;\n\n  @media (max-width: ", ") {\n    width: 6px;\n    height: 6px;\n    top: 35px;\n    left: 41px;\n  }\n\n  @keyframes blink-eye {\n    0% {\n      background: #e03e2f;\n      box-shadow: 0 0 10px #e03e2f;\n    }\n\n    50% {\n      background: #4a4d67;\n      box-shadow: none;\n    }\n\n    100% {\n      background: #e03e2f;\n      box-shadow: 0 0 10px #e03e2f;\n    }\n  }\n"], ["\n  width: 12px;\n  height: 12px;\n  border-radius: 50%;\n  position: absolute;\n  top: 70px;\n  left: 81px;\n  transform: translateZ(0);\n  animation: blink-eye 0.6s infinite;\n\n  @media (max-width: ", ") {\n    width: 6px;\n    height: 6px;\n    top: 35px;\n    left: 41px;\n  }\n\n  @keyframes blink-eye {\n    0% {\n      background: #e03e2f;\n      box-shadow: 0 0 10px #e03e2f;\n    }\n\n    50% {\n      background: #4a4d67;\n      box-shadow: none;\n    }\n\n    100% {\n      background: #e03e2f;\n      box-shadow: 0 0 10px #e03e2f;\n    }\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
var MessageContainer = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  align-self: center;\n  max-width: 480px;\n  margin-left: 40px;\n\n  @media (max-width: ", ") {\n    margin: 0;\n  }\n"], ["\n  align-self: center;\n  max-width: 480px;\n  margin-left: 40px;\n\n  @media (max-width: ", ") {\n    margin: 0;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
var Strikethrough = styled_1.default('span')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  text-decoration: line-through;\n"], ["\n  text-decoration: line-through;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=errorRobot.jsx.map