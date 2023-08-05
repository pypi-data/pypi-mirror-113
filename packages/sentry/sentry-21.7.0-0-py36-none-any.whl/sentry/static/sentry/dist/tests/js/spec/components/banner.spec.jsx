Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var enzyme_1 = require("sentry-test/enzyme");
var banner_1 = tslib_1.__importDefault(require("app/components/banner"));
describe('Banner', function () {
    it('can be dismissed', function () {
        var banner = enzyme_1.mountWithTheme(<banner_1.default dismissKey="test"/>);
        expect(banner.find('BannerWrapper').exists()).toBe(true);
        banner.find('CloseButton').simulate('click');
        expect(banner.find('BannerWrapper').exists()).toBe(false);
        expect(localStorage.getItem('test-banner-dismissed')).toBe('true');
    });
    it('is not dismissable', function () {
        var banner = enzyme_1.mountWithTheme(<banner_1.default isDismissable={false}/>);
        expect(banner.find('CloseButton').exists()).toBe(false);
    });
});
//# sourceMappingURL=banner.spec.jsx.map