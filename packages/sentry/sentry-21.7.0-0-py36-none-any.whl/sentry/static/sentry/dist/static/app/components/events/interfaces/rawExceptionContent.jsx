Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var clippedBox_1 = tslib_1.__importDefault(require("app/components/clippedBox"));
var rawStacktraceContent_1 = tslib_1.__importDefault(require("app/components/events/interfaces/rawStacktraceContent"));
var loadingError_1 = tslib_1.__importDefault(require("app/components/loadingError"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var locale_1 = require("app/locale");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var RawExceptionContent = /** @class */ (function (_super) {
    tslib_1.__extends(RawExceptionContent, _super);
    function RawExceptionContent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: false,
            error: false,
            crashReport: '',
        };
        return _this;
    }
    RawExceptionContent.prototype.componentDidMount = function () {
        if (this.isNative()) {
            this.fetchAppleCrashReport();
        }
    };
    RawExceptionContent.prototype.componentDidUpdate = function (prevProps) {
        if (this.isNative() && this.props.type !== prevProps.type) {
            this.fetchAppleCrashReport();
        }
    };
    RawExceptionContent.prototype.isNative = function () {
        var platform = this.props.platform;
        return platform === 'cocoa' || platform === 'native';
    };
    RawExceptionContent.prototype.getAppleCrashReportEndpoint = function (organization) {
        var _a = this.props, type = _a.type, projectId = _a.projectId, eventId = _a.eventId;
        var minified = type === 'minified';
        return "/projects/" + organization.slug + "/" + projectId + "/events/" + eventId + "/apple-crash-report?minified=" + minified;
    };
    RawExceptionContent.prototype.getContent = function (isNative, exc) {
        var type = this.props.type;
        var output = {
            downloadButton: null,
            content: exc.stacktrace
                ? rawStacktraceContent_1.default(type === 'original' ? exc.stacktrace : exc.rawStacktrace, this.props.platform, exc)
                : null,
        };
        if (!isNative) {
            return output;
        }
        var _a = this.state, loading = _a.loading, error = _a.error, crashReport = _a.crashReport;
        if (loading) {
            return tslib_1.__assign(tslib_1.__assign({}, output), { content: <loadingIndicator_1.default /> });
        }
        if (error) {
            return tslib_1.__assign(tslib_1.__assign({}, output), { content: <loadingError_1.default /> });
        }
        if (!loading && !!crashReport) {
            var _b = this.props, api = _b.api, organization = _b.organization;
            var downloadButton = null;
            if (organization) {
                var appleCrashReportEndpoint = this.getAppleCrashReportEndpoint(organization);
                downloadButton = (<DownloadBtnWrapper>
            <button_1.default size="xsmall" href={"" + api.baseUrl + appleCrashReportEndpoint + "&download=1"}>
              {locale_1.t('Download')}
            </button_1.default>
          </DownloadBtnWrapper>);
            }
            return {
                downloadButton: downloadButton,
                content: <clippedBox_1.default clipHeight={250}>{crashReport}</clippedBox_1.default>,
            };
        }
        return output;
    };
    RawExceptionContent.prototype.fetchAppleCrashReport = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, api, organization, data, _b;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization;
                        // Shared issues do not have access to organization
                        if (!organization) {
                            return [2 /*return*/];
                        }
                        this.setState({
                            loading: true,
                            error: false,
                            crashReport: '',
                        });
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise(this.getAppleCrashReportEndpoint(organization))];
                    case 2:
                        data = _c.sent();
                        this.setState({
                            error: false,
                            loading: false,
                            crashReport: data,
                        });
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        this.setState({ error: true, loading: false });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    RawExceptionContent.prototype.render = function () {
        var _this = this;
        var values = this.props.values;
        var isNative = this.isNative();
        if (!values) {
            return null;
        }
        return (<React.Fragment>
        {values.map(function (exc, excIdx) {
                var _a = _this.getContent(isNative, exc), downloadButton = _a.downloadButton, content = _a.content;
                if (!downloadButton && !content) {
                    return null;
                }
                return (<div key={excIdx}>
              {downloadButton}
              <pre className="traceback plain">{content}</pre>
            </div>);
            })}
      </React.Fragment>);
    };
    return RawExceptionContent;
}(React.Component));
exports.default = withApi_1.default(withOrganization_1.default(RawExceptionContent));
var DownloadBtnWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: flex-end;\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: flex-end;\n"])));
var templateObject_1;
//# sourceMappingURL=rawExceptionContent.jsx.map