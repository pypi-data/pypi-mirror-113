Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_select_1 = require("react-select");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var forms_1 = require("app/components/forms");
var timeSince_1 = tslib_1.__importDefault(require("app/components/timeSince"));
var version_1 = tslib_1.__importDefault(require("app/components/version"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
function VersionOption(_a) {
    var data = _a.data, props = tslib_1.__rest(_a, ["data"]);
    var release = data.release;
    return (<react_select_1.components.Option data={data} {...props}>
      <strong>
        <version_1.default version={release.version} anchor={false}/>
      </strong>
      <br />
      <small>
        {locale_1.t('Created')} <timeSince_1.default date={release.dateCreated}/>
      </small>
    </react_select_1.components.Option>);
}
var CustomResolutionModal = /** @class */ (function (_super) {
    tslib_1.__extends(CustomResolutionModal, _super);
    function CustomResolutionModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            version: '',
        };
        _this.onChange = function (value) {
            _this.setState({ version: value }); // TODO(ts): Add select value type as generic to select controls
        };
        _this.onAsyncFieldResults = function (results) {
            return results.map(function (release) { return ({
                value: release.version,
                label: release.version,
                release: release,
            }); });
        };
        return _this;
    }
    CustomResolutionModal.prototype.render = function () {
        var _this = this;
        var _a = this.props, orgSlug = _a.orgSlug, projectSlug = _a.projectSlug, closeModal = _a.closeModal, onSelected = _a.onSelected, Header = _a.Header, Body = _a.Body, Footer = _a.Footer;
        var url = projectSlug
            ? "/projects/" + orgSlug + "/" + projectSlug + "/releases/"
            : "/organizations/" + orgSlug + "/releases/";
        var onSubmit = function (e) {
            e.preventDefault();
            onSelected({ inRelease: _this.state.version });
            closeModal();
        };
        return (<form onSubmit={onSubmit}>
        <Header>{locale_1.t('Resolved In')}</Header>
        <Body>
          <forms_1.SelectAsyncField label={locale_1.t('Version')} id="version" name="version" onChange={this.onChange} placeholder={locale_1.t('e.g. 1.0.4')} url={url} onResults={this.onAsyncFieldResults} onQuery={function (query) { return ({ query: query }); }} components={{
                Option: VersionOption,
            }}/>
        </Body>
        <Footer>
          <button_1.default type="button" css={{ marginRight: space_1.default(1.5) }} onClick={closeModal}>
            {locale_1.t('Cancel')}
          </button_1.default>
          <button_1.default type="submit" priority="primary">
            {locale_1.t('Save Changes')}
          </button_1.default>
        </Footer>
      </form>);
    };
    return CustomResolutionModal;
}(React.Component));
exports.default = CustomResolutionModal;
//# sourceMappingURL=customResolutionModal.jsx.map