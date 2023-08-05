Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var eventDataSection_1 = tslib_1.__importDefault(require("app/components/events/eventDataSection"));
var richHttpContent_1 = tslib_1.__importDefault(require("app/components/events/interfaces/richHttpContent/richHttpContent"));
var utils_1 = require("app/components/events/interfaces/utils");
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var truncate_1 = tslib_1.__importDefault(require("app/components/truncate"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_2 = require("app/utils");
var RequestInterface = /** @class */ (function (_super) {
    tslib_1.__extends(RequestInterface, _super);
    function RequestInterface() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            view: 'formatted',
        };
        _this.isPartial = function () {
            // We assume we only have a partial interface is we're missing
            // an HTTP method. This means we don't have enough information
            // to reliably construct a full HTTP request.
            return !_this.props.data.method || !_this.props.data.url;
        };
        _this.toggleView = function (value) {
            _this.setState({
                view: value,
            });
        };
        return _this;
    }
    RequestInterface.prototype.render = function () {
        var _a = this.props, data = _a.data, type = _a.type;
        var view = this.state.view;
        var fullUrl = utils_1.getFullUrl(data);
        if (!utils_2.isUrl(fullUrl)) {
            // Check if the url passed in is a safe url to avoid XSS
            fullUrl = undefined;
        }
        var parsedUrl = null;
        if (fullUrl) {
            // use html tag to parse url, lol
            parsedUrl = document.createElement('a');
            parsedUrl.href = fullUrl;
        }
        var actions = null;
        if (!this.isPartial() && fullUrl) {
            actions = (<buttonBar_1.default merged active={view}>
          <button_1.default barId="formatted" size="xsmall" onClick={this.toggleView.bind(this, 'formatted')}>
            {/* Translators: this means "formatted" rendering (fancy tables) */}
            {locale_1.t('Formatted')}
          </button_1.default>
          <MonoButton barId="curl" size="xsmall" onClick={this.toggleView.bind(this, 'curl')}>
            curl
          </MonoButton>
        </buttonBar_1.default>);
        }
        var title = (<Header key="title">
        <externalLink_1.default href={fullUrl} title={fullUrl}>
          <Path>
            <strong>{data.method || 'GET'}</strong>
            <truncate_1.default value={parsedUrl ? parsedUrl.pathname : ''} maxLength={36} leftTrim/>
          </Path>
          {fullUrl && <StyledIconOpen size="xs"/>}
        </externalLink_1.default>
        <small>{parsedUrl ? parsedUrl.hostname : ''}</small>
      </Header>);
        return (<eventDataSection_1.default type={type} title={title} actions={actions} wrapTitle={false} className="request">
        {view === 'curl' ? (<pre>{utils_1.getCurlCommand(data)}</pre>) : (<richHttpContent_1.default data={data}/>)}
      </eventDataSection_1.default>);
    };
    return RequestInterface;
}(React.Component));
var MonoButton = styled_1.default(button_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  font-family: ", ";\n"], ["\n  font-family: ", ";\n"])), function (p) { return p.theme.text.familyMono; });
var Path = styled_1.default('span')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  text-transform: none;\n  font-weight: normal;\n\n  & strong {\n    margin-right: ", ";\n  }\n"], ["\n  color: ", ";\n  text-transform: none;\n  font-weight: normal;\n\n  & strong {\n    margin-right: ", ";\n  }\n"])), function (p) { return p.theme.textColor; }, space_1.default(0.5));
var Header = styled_1.default('h3')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
// Nudge the icon down so it is centered. the `external-icon` class
// doesn't quite get it in place.
var StyledIconOpen = styled_1.default(icons_1.IconOpen)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  transition: 0.1s linear color;\n  margin: 0 ", ";\n  color: ", ";\n  position: relative;\n  top: 1px;\n\n  &:hover {\n    color: ", ";\n  }\n"], ["\n  transition: 0.1s linear color;\n  margin: 0 ", ";\n  color: ", ";\n  position: relative;\n  top: 1px;\n\n  &:hover {\n    color: ", ";\n  }\n"])), space_1.default(0.5), function (p) { return p.theme.gray200; }, function (p) { return p.theme.subText; });
exports.default = RequestInterface;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=request.jsx.map