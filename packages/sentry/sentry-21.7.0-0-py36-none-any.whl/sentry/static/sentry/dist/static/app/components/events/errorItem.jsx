Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var startCase_1 = tslib_1.__importDefault(require("lodash/startCase"));
var moment_1 = tslib_1.__importDefault(require("moment"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var keyValueList_1 = tslib_1.__importDefault(require("app/components/events/interfaces/keyValueList"));
var metaProxy_1 = require("app/components/events/meta/metaProxy");
var listItem_1 = tslib_1.__importDefault(require("app/components/list/listItem"));
var eventErrors_1 = require("app/constants/eventErrors");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var externalLink_1 = tslib_1.__importDefault(require("../links/externalLink"));
var keyMapping = {
    image_uuid: 'Debug ID',
    image_name: 'File Name',
    image_path: 'File Path',
};
var ErrorItem = /** @class */ (function (_super) {
    tslib_1.__extends(ErrorItem, _super);
    function ErrorItem() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isOpen: false,
        };
        _this.handleToggle = function () {
            _this.setState({ isOpen: !_this.state.isOpen });
        };
        return _this;
    }
    ErrorItem.prototype.shouldComponentUpdate = function (_nextProps, nextState) {
        return this.state.isOpen !== nextState.isOpen;
    };
    ErrorItem.prototype.cleanedData = function (errorData) {
        var data = tslib_1.__assign({}, errorData);
        // The name is rendered as path in front of the message
        if (typeof data.name === 'string') {
            delete data.name;
        }
        if (data.message === 'None') {
            // Python ensures a message string, but "None" doesn't make sense here
            delete data.message;
        }
        if (typeof data.image_path === 'string') {
            // Separate the image name for readability
            var separator = /^([a-z]:\\|\\\\)/i.test(data.image_path) ? '\\' : '/';
            var path = data.image_path.split(separator);
            data.image_name = path.splice(-1, 1)[0];
            data.image_path = path.length ? path.join(separator) + separator : '';
        }
        if (typeof data.server_time === 'string' && typeof data.sdk_time === 'string') {
            data.message = locale_1.t('Adjusted timestamps by %s', moment_1.default
                .duration(moment_1.default.utc(data.server_time).diff(moment_1.default.utc(data.sdk_time)))
                .humanize());
        }
        return Object.entries(data).map(function (_a) {
            var _b = tslib_1.__read(_a, 2), key = _b[0], value = _b[1];
            return ({
                key: key,
                value: value,
                subject: keyMapping[key] || startCase_1.default(key),
                meta: metaProxy_1.getMeta(data, key),
            });
        });
    };
    ErrorItem.prototype.renderPath = function (data) {
        var name = data.name;
        if (!name || typeof name !== 'string') {
            return null;
        }
        return (<React.Fragment>
        <strong>{name}</strong>
        {': '}
      </React.Fragment>);
    };
    ErrorItem.prototype.renderTroubleshootingLink = function (error) {
        if (Object.values(eventErrors_1.JavascriptProcessingErrors).includes(error.type)) {
            return (<React.Fragment>
          {' '}
          (
          {locale_1.tct('see [docsLink]', {
                    docsLink: (<StyledExternalLink href="https://docs.sentry.io/platforms/javascript/sourcemaps/troubleshooting_js/">
                {locale_1.t('Troubleshooting for JavaScript')}
              </StyledExternalLink>),
                })}
          )
        </React.Fragment>);
        }
        return null;
    };
    ErrorItem.prototype.render = function () {
        var _a;
        var error = this.props.error;
        var isOpen = this.state.isOpen;
        var data = (_a = error === null || error === void 0 ? void 0 : error.data) !== null && _a !== void 0 ? _a : {};
        var cleanedData = this.cleanedData(data);
        return (<StyledListItem>
        <OverallInfo>
          <div>
            {this.renderPath(data)}
            {error.message}
            {this.renderTroubleshootingLink(error)}
          </div>
          {!!cleanedData.length && (<ToggleButton onClick={this.handleToggle} priority="link">
              {isOpen ? locale_1.t('Collapse') : locale_1.t('Expand')}
            </ToggleButton>)}
        </OverallInfo>
        {isOpen && <keyValueList_1.default data={cleanedData} isContextData/>}
      </StyledListItem>);
    };
    return ErrorItem;
}(React.Component));
exports.default = ErrorItem;
var ToggleButton = styled_1.default(button_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n  font-weight: 700;\n  color: ", ";\n  :hover,\n  :focus {\n    color: ", ";\n  }\n"], ["\n  margin-left: ", ";\n  font-weight: 700;\n  color: ", ";\n  :hover,\n  :focus {\n    color: ", ";\n  }\n"])), space_1.default(1.5), function (p) { return p.theme.subText; }, function (p) { return p.theme.textColor; });
var StyledListItem = styled_1.default(listItem_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(0.75));
var StyledExternalLink = styled_1.default(externalLink_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  /* && is here to increase specificity to override default styles*/\n  && {\n    font-weight: inherit;\n    color: inherit;\n    text-decoration: underline;\n  }\n"], ["\n  /* && is here to increase specificity to override default styles*/\n  && {\n    font-weight: inherit;\n    color: inherit;\n    text-decoration: underline;\n  }\n"])));
var OverallInfo = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: repeat(2, minmax(auto, max-content));\n  word-break: break-all;\n"], ["\n  display: grid;\n  grid-template-columns: repeat(2, minmax(auto, max-content));\n  word-break: break-all;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=errorItem.jsx.map