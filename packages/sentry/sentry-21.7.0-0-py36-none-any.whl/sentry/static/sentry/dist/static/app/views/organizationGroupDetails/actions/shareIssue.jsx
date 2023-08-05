Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/actions/button"));
var autoSelectText_1 = tslib_1.__importDefault(require("app/components/autoSelectText"));
var button_2 = tslib_1.__importDefault(require("app/components/button"));
var clipboard_1 = tslib_1.__importDefault(require("app/components/clipboard"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var dropdownLink_1 = tslib_1.__importDefault(require("app/components/dropdownLink"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var switchButton_1 = tslib_1.__importDefault(require("app/components/switchButton"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var ShareUrlContainer = /** @class */ (function (_super) {
    tslib_1.__extends(ShareUrlContainer, _super);
    function ShareUrlContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        // Select URL when its container is clicked
        _this.handleCopyClick = function () {
            var _a;
            (_a = _this.urlRef) === null || _a === void 0 ? void 0 : _a.selectText();
        };
        _this.handleUrlMount = function (ref) {
            var _a;
            _this.urlRef = ref;
            // Always select url if it's available
            (_a = _this.urlRef) === null || _a === void 0 ? void 0 : _a.selectText();
        };
        return _this;
    }
    ShareUrlContainer.prototype.render = function () {
        var _this = this;
        var _a = this.props, shareUrl = _a.shareUrl, onConfirming = _a.onConfirming, onCancel = _a.onCancel, onConfirm = _a.onConfirm;
        return (<UrlContainer>
        <TextContainer>
          <StyledAutoSelectText ref={function (ref) { return _this.handleUrlMount(ref); }}>
            {shareUrl}
          </StyledAutoSelectText>
        </TextContainer>

        <clipboard_1.default hideUnsupported value={shareUrl}>
          <ClipboardButton title={locale_1.t('Copy to clipboard')} borderless size="xsmall" onClick={this.handleCopyClick} icon={<icons_1.IconCopy />}/>
        </clipboard_1.default>

        <confirm_1.default message={locale_1.t('You are about to regenerate a new shared URL. Your previously shared URL will no longer work. Do you want to continue?')} onCancel={onCancel} onConfirming={onConfirming} onConfirm={onConfirm}>
          <ReshareButton title={locale_1.t('Generate new URL')} borderless size="xsmall" icon={<icons_1.IconRefresh />}/>
        </confirm_1.default>
      </UrlContainer>);
    };
    return ShareUrlContainer;
}(React.Component));
var ShareIssue = /** @class */ (function (_super) {
    tslib_1.__extends(ShareIssue, _super);
    function ShareIssue() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.hasConfirmModal = false;
        _this.handleToggleShare = function (e) {
            e.preventDefault();
            _this.props.onToggle();
        };
        _this.handleOpen = function () {
            var _a = _this.props, loading = _a.loading, isShared = _a.isShared, onToggle = _a.onToggle;
            if (!loading && !isShared) {
                // Starts sharing as soon as dropdown is opened
                onToggle();
            }
        };
        // State of confirm modal so we can keep dropdown menu opn
        _this.handleConfirmCancel = function () {
            _this.hasConfirmModal = false;
        };
        _this.handleConfirmReshare = function () {
            _this.hasConfirmModal = true;
        };
        return _this;
    }
    ShareIssue.prototype.render = function () {
        var _this = this;
        var _a = this.props, loading = _a.loading, isShared = _a.isShared, shareUrl = _a.shareUrl, onReshare = _a.onReshare, disabled = _a.disabled;
        return (<dropdownLink_1.default shouldIgnoreClickOutside={function () { return _this.hasConfirmModal; }} customTitle={<button_1.default disabled={disabled}>
            <DropdownTitleContent>
              <IndicatorDot isShared={isShared}/>
              {locale_1.t('Share')}
            </DropdownTitleContent>

            <icons_1.IconChevron direction="down" size="xs"/>
          </button_1.default>} onOpen={this.handleOpen} disabled={disabled} keepMenuOpen>
        <DropdownContent>
          <Header>
            <Title>{locale_1.t('Enable public share link')}</Title>
            <switchButton_1.default isActive={isShared} size="sm" toggle={this.handleToggleShare}/>
          </Header>

          {loading && (<LoadingContainer>
              <loadingIndicator_1.default mini/>
            </LoadingContainer>)}

          {!loading && isShared && shareUrl && (<ShareUrlContainer shareUrl={shareUrl} onCancel={this.handleConfirmCancel} onConfirming={this.handleConfirmReshare} onConfirm={onReshare}/>)}
        </DropdownContent>
      </dropdownLink_1.default>);
    };
    return ShareIssue;
}(React.Component));
exports.default = ShareIssue;
var UrlContainer = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: stretch;\n  border: 1px solid ", ";\n  border-radius: ", ";\n"], ["\n  display: flex;\n  align-items: stretch;\n  border: 1px solid ", ";\n  border-radius: ", ";\n"])), function (p) { return p.theme.border; }, space_1.default(0.5));
var LoadingContainer = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: center;\n"], ["\n  display: flex;\n  justify-content: center;\n"])));
var DropdownTitleContent = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  margin-right: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  margin-right: ", ";\n"])), space_1.default(0.5));
var DropdownContent = styled_1.default('li')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  padding: ", " ", ";\n\n  > div:not(:last-of-type) {\n    margin-bottom: ", ";\n  }\n"], ["\n  padding: ", " ", ";\n\n  > div:not(:last-of-type) {\n    margin-bottom: ", ";\n  }\n"])), space_1.default(1.5), space_1.default(2), space_1.default(1.5));
var Header = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n"], ["\n  display: flex;\n  justify-content: space-between;\n"])));
var Title = styled_1.default('h6')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  margin: 0;\n  padding-right: ", ";\n  white-space: nowrap;\n"], ["\n  margin: 0;\n  padding-right: ", ";\n  white-space: nowrap;\n"])), space_1.default(4));
var IndicatorDot = styled_1.default('span')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  display: inline-block;\n  margin-right: ", ";\n  border-radius: 50%;\n  width: 10px;\n  height: 10px;\n  background: ", ";\n"], ["\n  display: inline-block;\n  margin-right: ", ";\n  border-radius: 50%;\n  width: 10px;\n  height: 10px;\n  background: ", ";\n"])), space_1.default(0.5), function (p) { return (p.isShared ? p.theme.active : p.theme.border); });
var StyledAutoSelectText = styled_1.default(autoSelectText_1.default)(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n  padding: ", " 0 ", " ", ";\n  ", "\n"], ["\n  flex: 1;\n  padding: ", " 0 ", " ", ";\n  ", "\n"])), space_1.default(0.5), space_1.default(0.5), space_1.default(0.75), overflowEllipsis_1.default);
var TextContainer = styled_1.default('div')(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  display: flex;\n  flex: 1;\n  background-color: transparent;\n  border-right: 1px solid ", ";\n  max-width: 288px;\n"], ["\n  position: relative;\n  display: flex;\n  flex: 1;\n  background-color: transparent;\n  border-right: 1px solid ", ";\n  max-width: 288px;\n"])), function (p) { return p.theme.border; });
var ClipboardButton = styled_1.default(button_2.default)(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  border-radius: 0;\n  border-right: 1px solid ", ";\n  height: 100%;\n\n  &:hover {\n    border-right: 1px solid ", ";\n  }\n"], ["\n  border-radius: 0;\n  border-right: 1px solid ", ";\n  height: 100%;\n\n  &:hover {\n    border-right: 1px solid ", ";\n  }\n"])), function (p) { return p.theme.border; }, function (p) { return p.theme.border; });
var ReshareButton = styled_1.default(button_2.default)(templateObject_11 || (templateObject_11 = tslib_1.__makeTemplateObject(["\n  height: 100%;\n"], ["\n  height: 100%;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11;
//# sourceMappingURL=shareIssue.jsx.map